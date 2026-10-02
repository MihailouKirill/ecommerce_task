"""
File utility adapters for reading and parsing data.

This package contains infrastructure-specific implementations for
file operations, such as ZIP archive traversal and JSON parsing.
"""

from .json_parser import PandasJsonParser
from .zip_opener import ZipOpener

__all__: list[str] = ["PandasJsonParser", "ZipOpener"]
