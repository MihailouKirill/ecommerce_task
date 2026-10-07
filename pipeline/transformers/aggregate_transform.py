import pandas as pd

from pipeline.ports.transformer import TransformerPort


class AggregateTransform(TransformerPort):
    """
    Aggregates metrics by products category and customer segment.
    """

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates total revenue, units_sold, and unique_customers per group.

        Args:
            df:A DataFrame containing  enriched event data.

        Returns:
            pd.DataFrame: The aggregated DataFrame.

        """
        if df.empty:
            return df
        df = (
            df.groupby(["category", "segment", "customer_id"])
            .agg(
                total_revenue=("total_revenue", "sum"),
                units_sold=("quantity", "sum"),
            )
            .reset_index()
        )
        return df
