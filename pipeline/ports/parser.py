from abc import ABC, abstractmethod
from typing import IO

import pandas as pd


class BaseParser(ABC):
    """
    Port for parsing file streams into pandas DataFrames.
    """
    @abstractmethod
    def parse(self, file_stream: IO) -> pd.DataFrame:
        """
        Converts a raw file stream into a DataFrame.
        """
        pass
