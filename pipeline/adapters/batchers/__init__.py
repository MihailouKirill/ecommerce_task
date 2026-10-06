"""
Batching adapter.

Implementations for grouping data streams into batches.
"""
from .df_batcher import DFBatcher

__all__: list[str] = ["DFBatcher"]
