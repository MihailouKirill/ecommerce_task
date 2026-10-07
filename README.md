# E-commerce Sales ETL Pipeline

A production-ready ETL (Extract, Transform, Load) pipeline designed to process e-commerce sales data. The project is built following **Clean Architecture** principles to ensure high maintainability, testability, and decoupling of business logic from infrastructure.

## Technology Stack
- **Language:** Python 3.14
- **Package Manager:** `uv` (ultra-fast Rust-based package manager)
- **Data Processing:** `pandas` (batch processing for memory efficiency)
- **Database:** PostgreSQL 16
- **Configuration:** `pydantic-settings`
- **Infrastructure:** Docker & Docker Compose

## Architecture Design
The project strictly follows the **Dependency Inversion Principle** and uses a **Composition Root** pattern. 

- **`main.py` (Composition Root):** Acts strictly as an entry point. It wires up all infrastructure dependencies (database connections, file readers) and injects them into the Use Case.
- **`adapters/`:** Infrastructure layer. Contains implementations for reading ZIP files, parsing JSONs, and extracting reference data from PostgreSQL.
- **`ports/`:** Abstract interfaces defining the contract between the application core and external systems.
- **`transformers/`:** The core business rules. Pure, stateless data transformations (Filtering, Joining, Revenue Calculation, Aggregation).
- **`use_cases/`:** Orchestrates the ETL process using injected ports, ensuring the business logic knows nothing about SQL or the file system.

## Features
- **Batch Processing:** Reads and processes large event logs in memory-safe chunks (`BATCH_SIZE`).
- **Global Aggregation:** Accurately calculates metrics like unique customer counts across batched data.
- **Containerized Environment:** fully reproducible local setup with Docker. Database initialization (DDL/DML) is handled automatically.
## 🚀 Как запустить (Quick Start)

### Предварительные требования
Установленный **Docker** и **Docker Compose**.

### Запуск одной командой
В корневой папке проекта выполните:

```bash
docker compose up --build
```

## Project Structure
```text

ecommerce-task/
├── pipeline/
│   ├── adapters/       # DB extractors, File loaders, Parsers
│   ├── ports/          # Interfaces (BaseExtractor, LoaderPort)
│   ├── transformers/   # Business logic (JoinTransformer, FinalTransformer, etc.)
│   └── use_cases/      # main_pipeline.py (SalesReportUseCase)
├── sql/                # init.sql (Postgres initialization script)
├── tests/              # Unit tests for transformers and extractors
├── data/               # Raw input data (ZIP archives, JSON logs)
├── reports/            # Output directory for the final CSV report
├── main.py             # Entry point & Dependency Injection
├── docker-compose.yml  # Orchestrates PostgreSQL and the ETL app
├── Dockerfile          # Multi-stage build using `uv`
└── pyproject.toml      # Project metadata and dependencies

