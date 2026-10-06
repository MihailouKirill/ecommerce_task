import pandas as pd

from pipeline.ports.transformer import TransformerPort


class JoinTransformer(TransformerPort):
    """
    Joins event data with reference datasets(products and customers).
    """

    def __init__(self, products_df: pd.DataFrame, customers_df: pd.DataFrame) -> None:
        """
        Initializes the transformer with reference data.

        Args:
            products_df:DataFrame containing product reference data.
            customers_df:DataFrame containing customer reference data.
        """
        self.products_df = products_df
        self.customers_df = customers_df

    def transform(self, events_df: pd.DataFrame) -> pd.DataFrame:
        """
        Enriches events with product and customer reference data.

        Args:
            events_df:DataFrame containing event data.

        Returns:
            pd.DataFrame: The enriched DataFrame.
        """
        joined_df = pd.merge(events_df, self.products_df, on="product_id", how="left")
        joined_df = pd.merge(joined_df, self.customers_df, on="customer_id", how="left")
        return joined_df
