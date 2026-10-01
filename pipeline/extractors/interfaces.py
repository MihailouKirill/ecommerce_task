from abc import ABC, abstractmethod

import pandas as pd


class BaseExtractor(ABC):
    """
    Abstract interface for data extractors
    """

    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """
        Extracts data from the source

        Returns:
            pd.DataFrame: extracted data
        """
