"""
Main entry point and Composition Root for the Sales ETL pipeline.

This module is responsible only for wiring up infrastructure dependencies,
such as database connections and file readers. It injects these dependencies
into the main Use Case and triggers the execution.
"""

from pathlib import Path

from pipeline.adapters.batchers import DFBatcher
from pipeline.adapters.database import DataBasePostgreSQLConnection, SQLQueryValidator
from pipeline.adapters.extractors import DBExtractor, FileExtractor
from pipeline.adapters.loaders import FileLoader
from pipeline.adapters.parsers import PandasJsonParser
from pipeline.adapters.readers import ZipOpener
from pipeline.config import app_settings
from pipeline.use_cases import SalesReportUseCase


def main():
    """
    Initializes infrastructure adapters, assembles the ETL use case
    via Dependency Injection, and executes the pipeline.

    Steps performed:
        1. initializes database connection and SQL query validator.
        2. configures database extractors for reference data (products, customers).
        3. configures file extraction components for batch event processing.
        4. assembles the SalesReportUseCase using Dependency Injection (DI).
        5. executes the use case to generate the final sales report.

    """
    # 1. Initialize database connection and validator
    db_connection = DataBasePostgreSQLConnection(app_settings)
    validator = SQLQueryValidator()

    # 2. Configure extractors for reference data
    products_data_from_db = DBExtractor(
        db_connection,
        validator.validate_query("SELECT * FROM products"),
        app_settings.batch_size,
    )

    customers_data_from_db = DBExtractor(
        db_connection,
        validator.validate_query("SELECT * FROM customers"),
        app_settings.batch_size,
    )

    # 3. Initialize file extraction adapters
    zip_opener = ZipOpener(path=Path(__file__).resolve().parents[0] / "data")
    json_parser = PandasJsonParser()
    batcher = DFBatcher(app_settings.batch_size)
    events_data_from_file = FileExtractor(zip_opener, json_parser, batcher)
    file_loader = FileLoader(Path("reports/sales_report.csv"))

    # 4. Assemble the Use Case (Dependency Injection)
    use_case = SalesReportUseCase(
        events_data_from_file,
        products_data_from_db,
        customers_data_from_db,
        file_loader,
    )

    # 5. Execute the pipeline
    use_case.execute()


if __name__ == "__main__":
    main()
