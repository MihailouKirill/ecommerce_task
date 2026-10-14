"""
Bootstrap module (Composition Root).
Handles configuration reading and wires all infrastructure dependencies.
"""

import logging
from pathlib import Path

from pipeline.adapters.batchers import DFBatcher
from pipeline.adapters.compactor.csv_compactor import CSVReportCompactor
from pipeline.adapters.database import DataBasePostgreSQLConnection, SQLQueryValidator
from pipeline.adapters.extractors import DBExtractor, FileExtractor
from pipeline.adapters.loaders import FileLoader
from pipeline.adapters.parsers import PandasJsonParser
from pipeline.adapters.readers import ZipOpener
from pipeline.application.use_cases import SalesReportUseCase
from pipeline.config import Settings
from pipeline.domain.transformers import FinalTransformer

logger = logging.getLogger(__name__)


def build_use_case() -> SalesReportUseCase:
    """
    Assembles and wires the SalesReportUseCase with its required dependencies.

    Steps performed:
        1. Initializes the database connection and SQL query validator.
        2. Configures database extractors for reference data (products, customers).
        3. Configures file extraction components for batch event processing.
        4. Configures the file loader and CSV report compactor for output handling.
        5. Assembles the SalesReportUseCase using Dependency Injection (DI).
        6. Returns the fully initialized use case, ready for execution.

    Returns:
        SalesReportUseCase: Fully initialized use case instance ready for execution.
    """
    # 1. Initialize database connection and validator
    settings = Settings()

    db_connection = DataBasePostgreSQLConnection(
        db_host=settings.db_host,
        db_port=settings.db_port,
        db_user=settings.db_user,
        db_password=settings.db_password,
        db_name=settings.db_name,
    )

    validator = SQLQueryValidator()

    # 2. Configure extractors for reference data
    products_data_from_db = DBExtractor(
        db_connection,
        validator.validate_query("SELECT * FROM products"),
        settings.batch_size,
    )

    customers_data_from_db = DBExtractor(
        db_connection,
        validator.validate_query("SELECT * FROM customers"),
        settings.batch_size,
    )

    # 3. Configures file extraction components for batch event processing.

    zip_opener = ZipOpener(path=Path(__file__).resolve().parents[1] / "data")
    json_parser = PandasJsonParser()
    batcher = DFBatcher(settings.batch_size)
    events_data_from_file = FileExtractor(zip_opener, json_parser, batcher)

    # 4. Configures the file loader and CSV report compactor for output handling.
    report_path = Path(__file__).resolve().parents[1] / "reports" / "sales_report.csv"
    file_loader = FileLoader(report_path)

    file_compactor = CSVReportCompactor(
        file_path=report_path,
        final_transformer=FinalTransformer(),
        chunk_size=settings.batch_size,
    )

    logger.info("Dependencies assembled successfully. SalesReportUseCase is ready.")

    # 5. Assembles the SalesReportUseCase
    return SalesReportUseCase(
        events_extractor=events_data_from_file,
        products_extractor=products_data_from_db,
        customer_extractor=customers_data_from_db,
        loader=file_loader,
        compactor=file_compactor,
    )
