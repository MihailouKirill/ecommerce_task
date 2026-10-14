from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import Any


class IBaseExtractorPort[T](ABC):
    """
    Port for extracting data from external sources .
    """

    @abstractmethod
    def extract(self) -> Generator[T, Any, Any]:
        """
        Yields extracted data item by item.
        """
