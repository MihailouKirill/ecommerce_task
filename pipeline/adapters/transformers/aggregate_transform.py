import pandas as pd

from pipeline.ports.transformer import TransformerPort


class AggregateTransform(TransformerPort):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        df = (
            df.groupby(["category", "customer_segment"])
            .agg(
                total_revenue=("total_revenue", "sum"),
                units_sold=("quantity", "sum"),
                unique_customers=("customer_id", "nunique"),
            )
            .reset_index()
        )
        return df
