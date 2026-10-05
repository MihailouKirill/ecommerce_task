import pandas as pd

from pipeline.ports.transformer import TransformerPort


class PurchasesTransformer(TransformerPort):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        return df[df["event_type"] == "purchase"].copy()
