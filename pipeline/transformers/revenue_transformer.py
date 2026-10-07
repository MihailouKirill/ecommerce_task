import pandas as pd

from pipeline.ports.transformer import TransformerPort


class RevenueTransformer(TransformerPort):
    """
    Calculates the total revenue for each event.
    """

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Multiplies quantity and price to compute total revenue.

        Args:
            df:DataFrame containing 'quantity' and 'price' columns.

        Returns:
            pd.DataFrame containing 'total_revenue' column.
        """
        if df.empty:
            return df

        df = df.copy()
        df["total_revenue"] = df["quantity"] * df["price"]
        return df
