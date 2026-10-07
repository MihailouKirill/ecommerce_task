from abc import ABC, abstractmethod

import pandas as pd


class LoaderPort(ABC):
    """
    Port for data loading operations.
    """

    @abstractmethod
    def load(self, df: pd.DataFrame) -> None:
        """
        Saves the final DataFrame.

        Args:
            df:Processed DataFrame to save.
        """
