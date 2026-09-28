# 🚀 E-commerce Analytics Pipeline

Welcome to your data engineering project! The goal is to simulate a real-world commercial task by building a complete ETL (Extract, Transform, Load) pipeline.

You will be responsible for designing, building, and running a Python application that reads data from multiple sources (files and a database), processes it, and generates a final analysis report.

This project will challenge you to apply everything you've learned about **Python**, **OOP**, **SOLID**, **Pandas**, **NumPy**, and **PostgreSQL**.

## 🎯 Core Concepts to Apply

* **OOP (Object-Oriented Programming):** You will build a modular application using classes.
* **SOLID Principles:** Your code should be maintainable and extensible.
* **Pandas:** For loading, merging, and aggregating the data.
* **NumPy:** For efficient, vectorized numerical calculations.
* **PostgreSQL:** For connecting to, and reading from, a relational database.
* **Pydantic Settings:** For settings handling, using a `.env` file for configurations.

---

## 📖 The Task: Your Scenario

You are a data engineer at a new e-commerce company. Your data is fragmented:

1. **Business Data:** Your company's `product` catalog and `customer` information live in a production **PostgreSQL** database.
2. **Event Data:** All user activity (clicks, purchases) is dumped as JSON event logs into a complex, nested zip file structure.

**Your mission:** Create an automated pipeline that will be run daily. It must read all the event data, enrich it with data from the database, and produce a final CSV report summarizing sales performance by product category and customer segment.

---

## 🗃️ The Data Sources

You will be working with two distinct data sources.

### 1. File System: Event Logs

You must generate this data using the `data_generator.py` script.

* **Structure:** The script creates master zip files (e.g., `data/events_week_42.zip`).
* **Nesting:**
* Inside the master zip are **daily zip files** (e.g., `events_2023-10-23.zip`).
* Inside each daily zip are **JSON part-files** (e.g., `part-001.json`).


* **Event JSON Format:**
```json
[
  {
    "timestamp": "...",
    "customer_id": "c123",
    "event_type": "view_product",
    "product_id": "p789"
  },
  {
    "timestamp": "...",
    "customer_id": "c456",
    "event_type": "purchase",
    "product_id": "p101",
    "quantity": 2
  }
]

```



### 2. PostgreSQL Database

You will run a Docker container that automatically creates and populates this database using the `sql/init.sql` script.

* **`customers` table:** Contains information on all 100 customers.
| customer_id | join_date | segment |
| --- | --- | --- |
| c001 | 2024-12-05 | Regular |
| c002 | 2025-07-21 | VIP |
| ... | ... | ... |
| c100 | 2025-03-14 | New |


* **`products` table:** Contains information on all 50 products.
| product_id | product_name | category | price |
| --- | --- | --- | --- |
| p001 | Product Gamma 1 | Electronics | 149.99 |
| p002 | Product Alpha 2 | Books | 24.50 |
| ... | ... | ... | ... |
| p050 | Product Delta 50 | Electronics | 299.95 |



---

## 🛠️ 🐧 Setup: How to Get Started (Linux)

Follow these steps to set up your environment.

### Step 1: Set up the Python Environment

Let's create a virtual environment and install the dependencies.

```bash
# Synchronize packages via uv
uv sync

# Activate virtual environment if needed
source .venv/bin/activate

```

### Step 2: Start the Database

This project uses Docker to run the PostgreSQL database. The `docker-compose.yml` file is already configured.

```bash
# This command will start the database in the background.
# It will automatically find the `sql/init.sql` file and
# run it to create your tables and data.

docker compose up -d

```

Your database is now running. You can connect to it with these credentials:

* **Host:** `localhost`
* **Port:** `5432`
* **User:** `myuser`
* **Password:** `mypassword`
* **Database:** `ecommerce_db`

### Step 3: Generate the Event Data

Now, run the Python script to generate the raw event logs.

```bash
# This will create 50 weekly archives in a new 'data/' folder
python data_generator.py -c 50

```

---

## 🛠️ 🪟 Setup: How to Get Started (Windows)

Follow these steps to set up your environment on Windows.

> ⚠️ **Important:** Make sure you have Docker Desktop installed and running before you start.

### Step 1: Set up the Python Environment

Open your terminal (Command Prompt or PowerShell) to set up the uv environment.

```bash
# Synchronize packages via uv
uv sync

# Activate virtual environment if needed
.venv\Scripts\activate.bat
# Or .venv\Scripts\Activate.ps1 for powershell

```

### Step 2: Start the Database

This project uses Docker to run the PostgreSQL database. The `docker-compose.yml` file is already configured.

```bash
# This command will start the database in the background.
# It will automatically find the `sql/init.sql` file and
# run it to create your tables and data.

docker-compose up -d

```

### Step 3: Generate the Event Data

Now, run the Python script to generate the raw event logs.

```bash
# This will create 50 weekly archives in a new 'data/' folder
python data_generator.py -c 50

```

---

## 📋 Your Mission: The Pipeline

Your main task is to create the core pipeline logic (e.g., in a `pipeline/` directory). Your pipeline must perform these **Extract**, **Transform**, and **Load** steps:

1. **Extract (Files):** Create a class that can navigate the nested zip structure (`data/*.zip` -> `*.zip` -> `*.json`) and load all events into a single Pandas DataFrame.
2. **Extract (DB):** Create a class that connects to the PostgreSQL database and loads the `customers` and `products` tables into two separate DataFrames (hint: use `pd.read_sql`).
3. **Transform:**
* Filter the events DataFrame to get **only** `purchase` events.
* **Join** the `purchase` events with the `products` DataFrame on `product_id`.
* **Join** the result with the `customers` DataFrame on `customer_id`.
* **Feature Engineering:** Create a new column `total_revenue` = `quantity` * `price`.
* **Aggregate:** `groupby()` the DataFrame by `category` and `customer_segment`.
* **Count:** Calculate the `sum` of `total_revenue`, `sum` of `quantity` (as `units_sold`), and the `nunique` (count distinct) of `customer_id`.


4. **Load:** Save this final, aggregated DataFrame to a new file (e.g., `reports/sales_report.csv`).

---

## ⚙️ Engineering & Workflow Requirements

To elevate this project to a production-grade standard, you must integrate the following workflow strategies, optimization patterns, and architectural rules:

### 1. 🌿 Git Flow Development Model

You must maintain a structured development workflow using the following branch hierarchy:

* **`feature/*`:** Create dedicated short-lived branches for distinct units of work (e.g., `feature/extract-files`, `feature/db-connector`).
* **`dev`:** The primary integration branch where features are combined and validated.
* **`main`:** Represents stable production-ready code.
* > 🔍 **Note:** The Pull Request (PR) from `dev` -> `main` will serve as your final submission and will be reviewed thoroughly by your mentor. Direct commits to `main` or unauthorized merges are forbidden.



### 2. 🔄 Full Batch Execution Support (Memory Optimization)

To guarantee execution viability on weak machines or under scale, the entire pipeline cannot depend on processing all data continuously in RAM.

* **End-to-End Batching:** Implement a robust batch processing architecture using `itertools.batched` to handle the full sequence of the ETL flow (Extract, Transform, and Load by batches).
* Your data streams must be chunked sequentially from raw sources, transformed incrementally, and continuously loaded/appended to the destination target file to ensure predictable, bounded memory usage.

### 3. 📦 Package Code Architecture Compliance

Every Python package structure developed for this codebase must follow clean structural declaration practices:

* **Populated `__init__.py` files:** Do not leave package initialization files blank. Every `__init__.py` must contain comprehensive docstrings introducing and outlining the scope of that specific package.
* **Explicit Interface Control via `__all__`:** Explicitly declare the exposed public API elements using the `__all__: list[str]` boundary construct within every package initialization module.

---

## 🏁 Final Report (The Target)

| category | customer_segment | total_revenue | units_sold | unique_customers |
| --- | --- | --- | --- | --- |
| Electronics | VIP | 14999.50 | 120 | 45 |
| Electronics | New | 8500.00 | 70 | 60 |
| Clothing | Regular | 5200.25 | 210 | 115 |
| Books | Lapsed | 1500.75 | 80 | 30 |
| ... | ... | ... | ... | ... |

---

## ⭐ Bonus Challenges

If you finish the main task, try these:

* **Unit Testing:** Write `pytest` tests for your `DataTransformer` class.
* **Logging:** Add a proper `logging` module to your pipeline to log info and error messages.
* **Separate Reports:** Create a separate `report.csv` for each product category.
