"""
Adapters for the ETL pipeline.

Сoncrete implementations of the ports defined in the "pipeline.ports".

Adapters:
    DFBatcher: groups single DataFrames into batches.
    DataBasePostgreSQLConnection: context manager for PostgreSQL connection.
    SQLQueryValidator: validator for SQL queries.
    DBExtractor: extracts data from a database source.
    FileExtractor: extracts data from file source.
    PandasJsonParser: parses raw JSON data into a pandas DataFrame.
    ZipOpener: navigates and opens file streams from ZIP archives.
    AggregateTransform: aggregates metrics by category and customer segment.
    JoinTransformer: joins event data with reference datasets.
    RevenueTransformer: calculates revenue for events.
    PurchasesTransformer: filters events to include only purchases.
"""

from .batchers import DFBatcher
from .database import DataBasePostgreSQLConnection,SQLQueryValidator
from .extractors import DBExtractor, FileExtractor
from .parsers import PandasJsonParser
from .readers import ZipOpener
from .transformers import AggregateTransform,JoinTransformer,RevenueTransformer,PurchasesTransformer

__all__: list[str] = [
    "AggregateTransform",
    "DBExtractor",
    "DFBatcher",
    "DataBasePostgreSQLConnection",
    "FileExtractor",
    "JoinTransformer",
    "PandasJsonParser",
    "PurchasesTransformer",
    "RevenueTransformer",
    "SQLQueryValidator",
    "ZipOpener"
]