import pandas as pd

from pipeline.ports.transformer import TransformerPort


class PurchasesTransformer(TransformerPort):
    """
    Filters the events DataFrame to get only purchase events.
    """

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the Dataframe where event_type is 'purchase'.

        Args:
            df:Dataframe containing 'event_type' column.

        Returns:
            pd.DataFrame: Filtered Dataframe where 'event_type' is 'purchase'.
        """
        if df.empty:
            return df
        return df[df["event_type"] == "purchase"].copy().reset_index(drop=True)
