import pandas as pd

from pipeline.ports.transformer import TransformerPort


class JoinTransformer(TransformerPort):
    def __init__(self, products_df: pd.DataFrame, customers_df: pd.DataFrame) -> None:
        self.products_df = products_df
        self.customers_df = customers_df

    def transform(self, events_df: pd.DataFrame) -> pd.DataFrame:
        joined_df = pd.merge(events_df, self.products_df, on="product_id", how="left")
        joined_df = pd.merge(joined_df, self.customers_df, on="customer_id", how="left")
        return joined_df
