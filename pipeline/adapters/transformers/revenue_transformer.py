import pandas as pd

from pipeline.ports.transformer import TransformerPort


class RevenueTransformer(TransformerPort):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        df = df.copy()
        df["total_revenue"] = df["quantity"] * df["price"]
        return df
