from abc import ABC, abstractmethod
from typing import IO


class IBaseParserPort[T](ABC):
    """
    Port for parsing file streams into pandas DataFrames.
    """

    @abstractmethod
    def parse(self, file_stream: IO) -> T:
        """
        Converts a raw file stream into a DataFrame.
        """
