"""
Extractor adapters.

Concrete implementations for extracting data from external sources (databases, files).
"""

from .db_extractor import DBExtractor
from .file_extractor import FileExtractor

__all__: list[str] = [
    "DBExtractor",
    "FileExtractor"
]
