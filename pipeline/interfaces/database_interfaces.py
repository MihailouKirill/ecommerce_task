from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any


class DataBaseConnection(ABC):
    """
    Interface for creating the context manager for connecting to database
    """

    @abstractmethod
    def __enter__(self) -> Any:
        pass

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass


class QueryValidatorPort(ABC):
    """
    Interface for validating SQL queries before execution.
    """

    @abstractmethod
    def validate_query(self, query: str) -> str:
        pass
