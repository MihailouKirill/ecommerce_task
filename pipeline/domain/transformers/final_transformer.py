"""
Final report aggregation transformer.
"""
import logging
from collections.abc import Iterable

import pandas as pd

from pipeline.domain.ports.transformer import ITransformerPort

KEYS = ["category", "customer_segment", "customer_id"]
logger = logging.getLogger(__name__)


class FinalTransformer(ITransformerPort):
    """
    Merges partially aggregated batches into the final sales report.

    Performs bounded-memory iterative aggregation over incoming chunks
    and calculates final metrics including exact unique customer counts.
    """

    def __call__(self, data: Iterable[pd.DataFrame]) -> pd.DataFrame:
        """
        Folds partial batch aggregates into a consolidated sales report.

        Args:
            data: An iterable stream of DataFrame chunks containing partial batch aggregates.

        Returns:
            pd.DataFrame: Fully aggregated sales report grouped by category
            and customer segment, sorted alphabetically.
        """
        logger.info("Starting final report compaction...")
        acc = pd.DataFrame()

        for chunk in data:
            if chunk.empty:
                continue

            current_chunk = chunk
            if "segment" in chunk.columns and "customer_segment" not in chunk.columns:
                current_chunk = chunk.rename(columns={"segment": "customer_segment"})

            acc = (
                pd.concat([acc, current_chunk])
                .groupby(KEYS, as_index=False)[["total_revenue", "units_sold"]]
                .sum()
            )

        if acc.empty:
            logger.warning("No data encountered during final transformation.")
            return acc

        final_df = (
            acc.groupby(["category", "customer_segment"], as_index=False)
            .agg(
                total_revenue=("total_revenue", "sum"),
                units_sold=("units_sold", "sum"),
                unique_customers=("customer_id", "nunique"),
            )
            .round({"total_revenue": 2})
            .sort_values(["category", "customer_segment"], ignore_index=True)
        )
        final_df["units_sold"] = final_df["units_sold"].astype("int64")
        final_df["unique_customers"] = final_df["unique_customers"].astype("int64")

        logger.info("Final transformation completed.")
        return final_df
