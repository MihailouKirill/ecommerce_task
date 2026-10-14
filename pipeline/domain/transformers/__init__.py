"""
DataFrame transformers for the ETL pipeline.

Each transformer performs a single, distinct step in the ETL pipeline,
such as filtering purchase events, calculating total revenue, joining
reference dimensions, or aggregating data into the final report.
"""

from .aggregate_transform import AggregateTransform
from .final_transformer import FinalTransformer
from .join_transformer import JoinTransformer
from .revenue_transformer import RevenueTransformer
from .sales_transformer import PurchasesTransformer

__all__: list[str] = [
    "AggregateTransform",
    "FinalTransformer",
    "JoinTransformer",
    "PurchasesTransformer",
    "RevenueTransformer",
]
