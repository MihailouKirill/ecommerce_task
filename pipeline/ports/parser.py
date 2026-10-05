from abc import ABC, abstractmethod
from typing import IO

import pandas as pd


class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_stream: IO) -> pd.DataFrame:
        pass
