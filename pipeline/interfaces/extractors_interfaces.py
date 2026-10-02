from abc import ABC, abstractmethod
from collections.abc import Generator

import pandas as pd


class BaseExtractor(ABC):
    """
    Interface for data extractors
    """

    @abstractmethod
    def extract(self) -> Generator[pd.DataFrame]:
        pass
