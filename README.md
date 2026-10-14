# E-commerce Sales ETL Pipeline

A memory-bounded ETL (Extract, Transform, Load) pipeline that turns raw e-commerce
event logs and relational reference data into a sales report. It is built with
**Clean Architecture** and **SOLID** principles: business rules stay independent from
file, database and library details, and every external dependency can be swapped or
faked in tests.

## What it does

The pipeline is designed to run daily. It:

1. streams user events (clicks, purchases) from a nested ZIP structure,
2. enriches purchases with product and customer data from PostgreSQL,
3. aggregates sales by **product category** and **customer segment**,
4. writes the result to `reports/sales_report.csv`.

The main goal is **bounded memory usage**: the pipeline never loads all events into
RAM, so it keeps working on weak machines and as the data grows.

## Technology Stack

- **Language:** Python 3.14
- **Package manager:** `uv`
- **Data processing:** `pandas` (batch processing)
- **Database:** PostgreSQL 16
- **Configuration:** `pydantic-settings`
- **Infrastructure:** Docker & Docker Compose
- **Tests / quality:** `pytest`, `ty`, `ruff`

## Data sources

**1. Event logs (file system).** Master archives in `data/` contain daily ZIP files,
which in turn contain JSON part-files:

```text
data/events_week_42.zip
└── events_2023-10-23.zip
    └── part-001.json
```

Each JSON file is a list of events:

```json
[
  {"timestamp": "...", "customer_id": "c123", "event_type": "view_product", "product_id": "p789"},
  {"timestamp": "...", "customer_id": "c456", "event_type": "purchase", "product_id": "p101", "quantity": 2}
]
```

**2. PostgreSQL.** Initialized from `sql/init.sql`:

| Table | Columns |
|---|---|
| `customers` (100 rows) | `customer_id`, `join_date`, `segment` |
| `products` (50 rows) | `product_id`, `product_name`, `category`, `price` |

## How it works

### 1. Extract

- **Events** are read lazily. `ZipOpener` walks `data/*.zip -> *.zip -> *.json` and
  yields one open stream at a time, `PandasJsonParser` turns each stream into a
  DataFrame, and `DFBatcher` groups them with `itertools.batched` into batches of
  `BATCH_SIZE` files.
- **Reference data** (`products`, `customers`) is tiny (150 rows in total), so it is
  loaded once and kept in memory.

### 2. Transform (per batch)

Each batch passes through pure, stateless transformers:

1. `PurchasesTransformer` keeps only `purchase` events and casts `quantity` to `int`.
2. `JoinTransformer` left-joins products (`product_id`) and customers (`customer_id`).
3. `RevenueTransformer` computes `total_revenue = quantity * price`.
4. `AggregateTransform` groups by `(category, segment, customer_id)` and sums
   `total_revenue` and `units_sold`.

### 3. Load (per batch)

`FileLoader` writes the partial aggregate of every batch to `reports/sales_report.csv`:
the first batch creates the file (`mode="w"`, which also makes repeated runs
idempotent), all following batches are appended (`mode="a"`). After writing, the batch
is released with `del`, so only one batch lives in memory at a time.

### 4. Compact

The file now holds partial aggregates, so the same group can appear in several
batches. `CSVReportCompactor` reads it back **in chunks**, and `FinalTransformer`
folds the chunks into a running accumulator and computes the final metrics. The result
replaces the file atomically (write to `.tmp.csv`, then `replace`).

> **Why aggregate by customer first?** `unique_customers` is a distinct count, and
> distinct counts cannot be summed across batches (the same customer may appear in
> many of them). Keeping `customer_id` in the partial aggregates makes the final
> `nunique` exact, while the accumulator stays small: at most
> `categories x segments x customers` rows, regardless of how many events were processed.

## Output

`reports/sales_report.csv`, one row per `(category, customer_segment)`:

| Column | Type | Description |
|---|---|---|
| `category` | str | Product category |
| `customer_segment` | str | Customer segment (`New`, `Regular`, `VIP`, `Lapsed`) |
| `total_revenue` | float | Sum of `quantity * price` per group, rounded to 2 decimals |
| `units_sold` | int | Sum of purchased quantities |
| `unique_customers` | int | Distinct customers who purchased in the group |

Example:

```csv
category,customer_segment,total_revenue,units_sold,unique_customers
Books,Lapsed,285908.26,1216,28
Books,New,250916.1,1074,24
```

## Architecture

The project follows Clean Architecture principles. Dependencies point strictly inward:
adapters implement application ports, the use case orchestrates the pipeline through
abstractions, and the domain layer stays completely isolated from external technologies.

- **Domain layer (`pipeline/domain/`)**: the innermost layer, with no file, database
  or network access and no dependencies on outer layers.
  - `ports/`: declares the domain contract `ITransformerPort[T]`.
  - `transformers/`: pure, stateless DataFrame transformations that enforce business
    logic: `PurchasesTransformer`, `JoinTransformer`, `RevenueTransformer`,
    `AggregateTransform` and `FinalTransformer`.
- **Application layer (`pipeline/application/`)**: orchestration logic and boundary
  contracts.
  - `ports/`: boundary interfaces for all external technologies (`IBaseExtractorPort`,
    `ILoaderPort`, `ICompactorPort`, `IFileReaderPort`, `IBaseParserPort`,
    `IBatcherPort`, `IDataBaseConnectionPort`, `IQueryValidatorPort`, `IUseCasePort`).
  - `use_cases/`: `SalesReportUseCase` coordinates extraction, transformation, loading
    and compaction using only injected port interfaces.
- **Adapters layer (`pipeline/adapters/`)**: connects the application to concrete
  technologies (PostgreSQL, ZIP archives, JSON and CSV formats, and pandas). Every
  adapter implements a port declared in the application layer. Replacing a storage
  backend (e.g. swapping CSV output for Parquet) requires writing a new adapter and
  updating a single line in `bootstrap.py`.
  - `readers/`: `ZipOpener` walks nested archives (`data/*.zip` -> daily ZIP -> JSON)
    and yields one open file stream at a time.
  - `parsers/`: `PandasJsonParser` turns a JSON stream into a DataFrame.
  - `batchers/`: `DFBatcher` groups parsed DataFrames into batches of `BATCH_SIZE`
    using `itertools.batched`.
  - `extractors/`: `FileExtractor` chains opener, parser and batcher into a lazy event
    stream; `DBExtractor` runs SQL queries and yields chunks.
  - `database/`: `DataBasePostgreSQLConnection` manages connections (commit on
    success, rollback on error); `SQLQueryValidator` validates `SELECT` queries.
  - `loaders/`: `FileLoader` writes partial aggregates to the report CSV (creates the
    file on the first batch, appends on subsequent batches).
  - `compactor/`: `CSVReportCompactor` streams the accumulated CSV in chunks, applies
    the final aggregation and atomically replaces the output file.
- **Composition root and entry point**
  - `pipeline/bootstrap.py`: reads `Settings`, instantiates concrete adapters and wires
    them into the use case. This is the only module aware of concrete classes across
    all layers.
  - `pipeline/config.py`: application configuration powered by `pydantic-settings`.
  - `main.py`: executable entry point that constructs and runs the use case.

## Project structure

```text
.
├── data/                            # Source ZIP files with events
├── pipeline/                        # Core application code
│   ├── adapters/                    # Infrastructure adapters
│   │   ├── batchers/                # Groups parsed streams into DataFrame batches
│   │   │   ├── __init__.py
│   │   │   └── df_batcher.py
│   │   ├── compactor/               # Chunked CSV consolidation adapter
│   │   │   ├── __init__.py
│   │   │   └── csv_compactor.py
│   │   ├── database/                # PostgreSQL connection context manager & SQL validator
│   │   │   ├── __init__.py
│   │   │   ├── postgres_connection.py
│   │   │   └── query_validator.py
│   │   ├── extractors/              # DB and file stream extractors
│   │   │   ├── __init__.py
│   │   │   ├── db_extractor.py
│   │   │   └── file_extractor.py
│   │   ├── loaders/                 # File writer adapter
│   │   │   ├── __init__.py
│   │   │   └── file_loader.py
│   │   ├── parsers/                 # JSON parser adapter
│   │   │   ├── __init__.py
│   │   │   └── json_parser.py
│   │   ├── readers/                 # Nested ZIP archive opener
│   │   │   ├── __init__.py
│   │   │   └── zip_opener.py
│   │   └── __init__.py
│   ├── application/                 # Application layer
│   │   ├── ports/                   # Contracts for extractors, loaders, DB, use case
│   │   │   ├── __init__.py
│   │   │   ├── batcher.py
│   │   │   ├── compactor.py
│   │   │   ├── database_connection.py
│   │   │   ├── extractor.py
│   │   │   ├── loader.py
│   │   │   ├── parser.py
│   │   │   ├── query_validator.py
│   │   │   ├── readers.py
│   │   │   └── use_case.py
│   │   ├── use_cases/               # SalesReportUseCase pipeline orchestrator
│   │   │   ├── __init__.py
│   │   │   └── main_pipeline.py
│   │   └── __init__.py
│   ├── domain/                      # Pure business logic
│   │   ├── ports/                   # Domain transformer contracts
│   │   │   ├── __init__.py
│   │   │   └── transformer.py
│   │   ├── transformers/            # Pure DataFrame transformations
│   │   │   ├── __init__.py
│   │   │   ├── aggregate_transform.py
│   │   │   ├── final_transformer.py
│   │   │   ├── join_transformer.py
│   │   │   ├── revenue_transformer.py
│   │   │   └── sales_transformer.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── bootstrap.py                 # Composition root (wires all dependencies)
│   └── config.py                    # Pydantic settings
├── reports/                         # Output directory for the final CSV
├── sql/                             # DB initialization script
├── tests/                           # Unit tests
├── .env.example                     # Environment variables template
├── data_generator.py                # Generates the event archives
├── docker-compose.yml               # PostgreSQL + the pipeline
├── Dockerfile                       # Application image build instructions
├── main.py                          # Entry point
├── pyproject.toml                   # Dependencies and project metadata
└── README.md                        # Project documentation
```

Every package has a documented `__init__.py` with an explicit `__all__: list[str]`.

## Configuration

Settings come from environment variables or, for local runs, from a `.env` file in
the project root (see `.env.example`). Docker Compose passes them as environment
variables, so no `.env` is needed there.

| Variable | Default | Description |
|---|---|---|
| `DB_HOST` | required | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_USER` | required | PostgreSQL user |
| `DB_PASSWORD` | required | PostgreSQL password |
| `DB_NAME` | required | PostgreSQL database name |
| `BATCH_SIZE` | `100` (code default), `50` in `.env.example` and Compose | Number of JSON files per event batch; also the row chunk size for DB reads and for compaction |

`BATCH_SIZE` is the knob that trades memory for speed: smaller values use less RAM,
larger values mean fewer iterations. The credentials in `docker-compose.yml` and
`.env.example` are demo values for local development only.

## Quick start

The event archives are **not** baked into the Docker image: `data/` is mounted into
the container, so generate it first (this step needs a local Python environment):

```bash
uv sync
uv run python data_generator.py -c 50     # creates 50 weekly archives in data/
```

### Docker (recommended)

```bash
docker compose up --build
```

No `.env` file is needed: the database credentials and `BATCH_SIZE` are set in
`docker-compose.yml`. Compose starts two services:

| Service | Description |
|---|---|
| `db` | PostgreSQL 16, filled from `sql/init.sql` on first start; has a health check |
| `etl_pipeline` | Waits for a healthy `db`, runs the pipeline, then exits; `./data` and `./reports` are mounted from the host |

The report appears in `reports/sales_report.csv`. To stop the database, run
`docker compose down` (add `-v` to also delete the DB volume; `init.sql` runs again on
the next start with an empty volume).

### Local run

```bash
cp .env.example .env              # DB_HOST=localhost
docker compose up -d db           # start only PostgreSQL, not the pipeline
uv run python main.py
```

On Windows, use `docker-compose` if `docker compose` is not available, and make sure
Docker Desktop is running. Port `5432` must be free on the host.

## Development

```bash
uv run pytest        # unit tests
uv run ty check      # static type checking
uv run ruff check .  # linting
```

Tests cover the domain transformers (including the exact cross-batch
`unique_customers` count with a one-shot iterator), the file extractor with fake
opener/parser/batcher, and the PostgreSQL connection manager (commit/rollback).

**Git Flow:** `feature/*` -> `dev` -> `main`. The `dev -> main` pull request is the
final submission; direct commits to `main` are not allowed.

## Design decisions

- **End-to-end laziness.** Extraction is a chain of generators, transformation works
  on one batch, loading appends to the file. Nothing materializes the full dataset.
- **Two-phase output.** Partial aggregates are appended batch by batch (bounded
  memory), then compacted once into the final report. This keeps the distinct count
  correct.
- **Safe reruns.** The first write of a run truncates the file, and the final report
  is swapped in atomically, so repeated runs do not duplicate data.
- **Compaction in `finally`.** The use case always attempts compaction, even if a batch
  fails midway.
- **Pure domain.** Transformers never touch files or the database and are tested with
  small in-memory DataFrames.