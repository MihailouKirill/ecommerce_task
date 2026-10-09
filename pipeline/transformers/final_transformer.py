import pandas as pd

from pipeline.ports.transformer import TransformerPort


class FinalTransformer(TransformerPort):
    """
    Performs final aggregation and formatting for the sales report.
    """

    def __call__(self, final_raw_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates final unique customers and formats the report.

        Args:
        final_raw_df: DataFrame containing concatenated batches with partially aggregated data.

        Returns:
        pd.DataFrame: The fully aggregated and formatted DataFrame.
        """
        if final_raw_df.empty:
            return final_raw_df

        final_df = final_raw_df.groupby(["category", "segment"], as_index=False).agg(
            total_revenue=("total_revenue", "sum"),
            units_sold=("units_sold", "sum"),
            unique_customers=("customer_id", "nunique"),
        )

        final_df = final_df.rename(columns={"segment": "customer_segment"})
        final_df["total_revenue"] = final_df["total_revenue"].fillna(0).round(2)
        final_df["units_sold"] = final_df["units_sold"].fillna(0).astype(int)

        return final_df
