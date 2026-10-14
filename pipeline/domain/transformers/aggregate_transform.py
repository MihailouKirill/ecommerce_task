import pandas as pd

from pipeline.domain.ports.transformer import ITransformerPort


class AggregateTransform(ITransformerPort):
    """
    Aggregates metrics by products category and customer segment.
    """

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates total revenue, units_sold, and unique_customers per group.

        Args:
            data:A DataFrame containing  enriched event data.

        Returns:
            pd.DataFrame: The aggregated DataFrame.

        """
        if data.empty:
            return data
        data = (
            data.groupby(["category", "segment", "customer_id"])
            .agg(
                total_revenue=("total_revenue", "sum"),
                units_sold=("quantity", "sum"),
            )
            .reset_index()
        )
        return data
