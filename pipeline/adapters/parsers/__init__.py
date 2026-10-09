"""
Parser adapters.

Concrete implementations for parsing raw file streams into pandas DataFrames.
"""

from .json_parser import PandasJsonParser

__all__ = ["PandasJsonParser"]
