"""
Adapters for the ETL pipeline.

Concrete implementations of infrastructure ports declared in pipeline.application.ports.

Adapters:
    DFBatcher: Groups single DataFrames into batches of a given size.
    CSVReportCompactor: Consolidated chunked CSV report files atomically.
    DataBasePostgreSQLConnection: Context manager for PostgreSQL connection lifecycle.
    SQLQueryValidator: Validates and normalizes SQL queries.
    DBExtractor: Extracts data in batches from a database source.
    FileExtractor: Extracts event data streams lazily from file archives.
    FileLoader: Saves DataFrame batches to disk in CSV format.
    PandasJsonParser: Parses raw JSON streams into pandas DataFrames.
    ZipOpener: Navigates and opens file streams inside nested ZIP archives.
"""

from .batchers import DFBatcher
from .compactor import CSVReportCompactor
from .database import DataBasePostgreSQLConnection, SQLQueryValidator
from .extractors import DBExtractor, FileExtractor
from .loaders import FileLoader
from .parsers import PandasJsonParser
from .readers import ZipOpener

__all__: list[str] = [
    "CSVReportCompactor",
    "DBExtractor",
    "DFBatcher",
    "DataBasePostgreSQLConnection",
    "FileExtractor",
    "FileLoader",
    "PandasJsonParser",
    "SQLQueryValidator",
    "ZipOpener",
]