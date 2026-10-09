# E-commerce Sales ETL Pipeline

A production-ready ETL (Extract, Transform, Load) pipeline designed to process e-commerce sales data. The project is built following **Clean Architecture** principles to ensure high maintainability, testability, and decoupling of business logic from infrastructure.

## Technology Stack
- **Language:** Python 3.14
- **Package Manager:** `uv` 
- **Data Processing:** `pandas` (batch processing for memory efficiency)
- **Database:** PostgreSQL 16
- **Configuration:** `pydantic-settings`
- **Infrastructure:** Docker & Docker Compose

## Architecture Design
The project strictly follows Clean Architecture to separate business logic from infrastructure details:

- **`pipeline/ports/`**: Interfaces defining contracts for extractors, loaders, transformers, and database connections.
- **`pipeline/adapters/`**: Infrastructure layer implementations. Contains DB extractors, file loaders, parsers, and batchers.
- **`pipeline/transformers/`**: Application services. Pure DataFrame transformations (filter, join, compute revenue, aggregate). They implement `TransformerPort` but encode business rules, remaining stateless with respect to the input DataFrame.
- **`pipeline/use_cases/`**: Contains the core orchestrator (`main_pipeline.py`) that executes the ETL steps via injected dependencies.
- **`main.py`**: The Entry Point and Composition Root. It initializes dependencies and injects them into the Use Case.

## How it works

1. **Extract:** Loads `products` and `customers` from PostgreSQL (small, kept in memory), and streams `events` from ZIP archives in `data/` in batches.
2. **Transform:** Filters purchase events, joins with product and customer data, computes `total_revenue = quantity * price`.
3. **Aggregate:** Groups by `category` and `customer_segment`, computing `total_revenue`, `units_sold`, and `unique_customers`. (Maintains per-group sets of customer IDs across batches to compute accurate `nunique`).
4. **Load:** Writes the final report to `reports/sales_report.csv`.

### Output schema

| Column | Type | Description |
|---|---|---|
| `category` | str | Product category |
| `customer_segment` | str | Customer segment (VIP, New, Regular) |
| `total_revenue` | float | Sum of revenue per group |
| `units_sold` | int | Sum of quantities sold |
| `unique_customers` | int | Distinct customers per group |

## Quick Start (Docker)

The project is fully containerized. You do not need Python or PostgreSQL installed locally.

### 1. Start the Pipeline
Run the following command in the root directory:

```bash
docker compose up --build
```

## Project Structure
```text
task/
├── data/                            # Source ZIP files with events
├── pipeline/                        # Core application code
│   ├── adapters/                    # Infrastructure layer
│   │   ├── batchers/
│   │   │   ├── __init__.py
│   │   │   └── df_batcher.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── postgres_connection.py
│   │   │   └── query_validator.py
│   │   ├── extractors/
│   │   │   ├── __init__.py
│   │   │   ├── db_extractor.py
│   │   │   └── file_extractor.py
│   │   ├── loaders/
│   │   │   ├── __init__.py
│   │   │   └── file_loader.py
│   │   ├── parsers/
│   │   │   ├── __init__.py
│   │   │   └── json_parser.py
│   │   ├── readers/
│   │   │   ├── __init__.py
│   │   │   └── zip_opener.py
│   │   ├── transformers/            # Business logic DataFrame transformers
│   │   │   ├── __init__.py
│   │   │   ├── aggregate_transform.py
│   │   │   ├── final_transformer.py
│   │   │   ├── join_transformer.py
│   │   │   ├── revenue_transformer.py
│   │   │   └── sales_transformer.py
│   │   └── __init__.py
│   ├── ports/                       # Interfaces defining contracts
│   │   ├── __init__.py
│   │   ├── batcher.py
│   │   ├── database_connection.py
│   │   ├── extractor.py
│   │   ├── loader.py
│   │   ├── parser.py
│   │   ├── query_validator.py
│   │   ├── readers.py
│   │   ├── transformer.py
│   │   └── use_case.py
│   ├── use_cases/                   # ETL orchestration
│   │   ├── __init__.py
│   │   └── main_pipeline.py
│   ├── __init__.py
│   └── config.py                    # Pydantic settings
├── reports/                         # Output directory for the final CSV
│   └── sales_report.csv
├── sql/                             # Database initialization script
│   └── init.sql
├── tests/                           # Unit tests
│   ├── __init__.py
│   ├── test_db_connection.py
│   ├── test_file_extract.py
│   └── test_sales_transformer.py
├── .dockerignore
├── .env                             # Environment variables
├── .gitignore
├── docker-compose.yml               # Services configuration
├── Dockerfile                       # Application image build instructions
├── install.cmd                      # Helper installation script
├── main.py                          # Entry point & Composition Root
├── pyproject.toml                   # Dependencies and project metadata
├── README.md                        # Project documentation
└── uv.lock                          # Dependency lock file

