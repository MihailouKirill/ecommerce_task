import pandas as pd

from pipeline.domain.ports.transformer import ITransformerPort


class RevenueTransformer(ITransformerPort):
    """
    Calculates the total revenue for each event.
    """

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Multiplies quantity and price to compute total revenue.

        Args:
            data:DataFrame containing 'quantity' and 'price' columns.

        Returns:
            pd.DataFrame containing 'total_revenue' column.
        """
        if data.empty:
            return data

        data = data.copy()
        data["total_revenue"] = data["quantity"] * data["price"]
        return data
