"""
Ports for the ETL pipeline

Each port defines a contract that adapters in "pipeline.adapters" must implement.
The core layer depends only on these abstractions, not on concrete implementations.
"""

from .batcher import BatcherPort
from .database_connection import DataBaseConnection
from .extractor import BaseExtractor
from .loader import LoaderPort
from .parser import BaseParser
from .query_validator import QueryValidatorPort
from .readers import FileReaderPort
from .transformer import TransformerPort

__all__: list[str] = [
    "BaseExtractor",
    "BaseParser",
    "BatcherPort",
    "DataBaseConnection",
    "FileReaderPort",
    "LoaderPort",
    "QueryValidatorPort",
    "TransformerPort",
]
