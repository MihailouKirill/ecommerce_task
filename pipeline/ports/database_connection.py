from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any


class DataBaseConnection(ABC):
    """
    Port for database connection context manager.
    """

    @abstractmethod
    def __enter__(self) -> Any:
        """Opens and returns the database connection."""
        pass

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Commits or rolls back the transaction and closes the connection."""
        pass
