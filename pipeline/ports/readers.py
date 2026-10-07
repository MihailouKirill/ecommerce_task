from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import IO


class FileReaderPort(ABC):
    """
    Port for file reading operations.
    """

    @abstractmethod
    def open(self) -> Iterator[IO]:
        """
        Opens the source and yields raw file stream.
        """
