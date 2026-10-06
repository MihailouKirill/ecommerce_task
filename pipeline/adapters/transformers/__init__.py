"""
Transformation adapters for data processing.

Each transformer is strickly responsible for a single, distinct step
in the ETL pipeline, such as filtering events, calculating revenue,
joining reference data, or aggregating final table.
"""
from .aggregate_transform import AggregateTransform
from .join_transformer import JoinTransformer
from .revenue_transformer import RevenueTransformer
from .sales_transformer import PurchasesTransformer

__all__ = [
    "AggregateTransform",
    "JoinTransformer",
    "PurchasesTransformer",
    "RevenueTransformer",
]
