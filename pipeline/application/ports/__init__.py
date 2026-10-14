"""
Application ports for the ETL pipeline.

Each port defines a contract that adapters in "pipeline.adapters" must implement
or that application use cases expose. The application core depends only on these
abstractions, not on concrete implementations.
"""
from .batcher import IBatcherPort
from .compactor import ICompactorPort
from .database_connection import IDataBaseConnectionPort
from .extractor import IBaseExtractorPort
from .loader import ILoaderPort
from .parser import IBaseParserPort
from .query_validator import IQueryValidatorPort
from .readers import IFileReaderPort
from .use_case import IUseCasePort

__all__: list[str] = [
    "IBaseExtractorPort",
    "IBaseParserPort",
    "IBatcherPort",
    "ICompactorPort",
    "IDataBaseConnectionPort",
    "IFileReaderPort",
    "ILoaderPort",
    "IQueryValidatorPort",
    "IUseCasePort",
]
