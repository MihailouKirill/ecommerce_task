import pandas as pd

from pipeline.domain.ports.transformer import ITransformerPort


class PurchasesTransformer(ITransformerPort):
    """
    Filters the events DataFrame to get only purchase events.
    """

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the Dataframe where event_type is 'purchase'.

        Args:
            data:Dataframe containing 'event_type' column.

        Returns:
            pd.DataFrame: Filtered Dataframe where 'event_type' is 'purchase'.
        """
        if data.empty:
            return data
        filtered = data[data["event_type"] == "purchase"].copy().reset_index(drop=True)

        if not filtered.empty:
            filtered["quantity"] = filtered["quantity"].astype("int64")

        return filtered
