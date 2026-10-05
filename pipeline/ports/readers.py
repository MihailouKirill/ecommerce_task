from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import IO


class FileReaderPort(ABC):
    """
    Interface for file reading operations.
    """

    @abstractmethod
    def open(self) -> Iterator[IO]:
        pass
