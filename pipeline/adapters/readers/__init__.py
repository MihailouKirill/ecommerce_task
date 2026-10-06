"""
Reader adapters.

Concrete implementations for infrastructure file operations,
such as directory traversal and nested ZIP archive handling.
"""

from .zip_opener import ZipOpener

__all__: list[str] = ["ZipOpener"]
