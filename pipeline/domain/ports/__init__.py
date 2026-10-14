"""
Package for domain interface ports.

Defines contracts for domain-level operations and transformations.
"""

from .transformer import ITransformerPort

__all__: list[str] = ["ITransformerPort"]
