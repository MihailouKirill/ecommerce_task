from abc import ABC, abstractmethod

import pandas as pd


class TransformerPort(ABC):
    """
    Port for data transformation operations.
    """
    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies transformation logic to the given DataFrame.
        """
        pass
