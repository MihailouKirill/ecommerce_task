from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import Any


class BaseExtractor[T](ABC):
    """
    Interface for data extractors
    """

    @abstractmethod
    def extract(self) -> Generator[T, Any, Any]:
        pass
