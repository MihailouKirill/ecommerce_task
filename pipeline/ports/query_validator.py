from abc import ABC, abstractmethod


class QueryValidatorPort(ABC):
    """
    Interface for validating SQL queries before execution.
    """

    @abstractmethod
    def validate_query(self, query: str) -> str:
        pass
