from abc import ABC, abstractmethod
from collections.abc import Generator, Iterable

import pandas as pd


class BatcherPort(ABC):
    """
    Interface for batching streams of DataFrames.
    """

    @abstractmethod
    def batch(
        self, items: Iterable[pd.DataFrame]
    ) -> Generator[pd.DataFrame]:
        pass
