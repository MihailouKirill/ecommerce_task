"""
Loader adapters.

Concrete implementation for exporting and saving processed data.
"""

from .file_loader import FileLoader

__all__: list[str] = ["FileLoader"]
