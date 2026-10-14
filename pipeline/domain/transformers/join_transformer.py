import pandas as pd

from pipeline.domain.ports.transformer import ITransformerPort


class JoinTransformer(ITransformerPort):
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

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Enriches events with product and customer reference data.

        Args:
            data:DataFrame containing event data.

        Returns:
            pd.DataFrame: The enriched DataFrame.
        """
        joined_df = pd.merge(data, self.products_df, on="product_id", how="left")
        joined_df = pd.merge(joined_df, self.customers_df, on="customer_id", how="left")
        return joined_df
