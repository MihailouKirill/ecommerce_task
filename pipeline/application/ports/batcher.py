from abc import ABC, abstractmethod
from collections.abc import Generator, Iterable


class IBatcherPort[T](ABC):
    """
    Port for grouping  DataFrames into batches.
    """

    @abstractmethod
    def batch(self, items: Iterable[T]) -> Generator[T]:
        pass
