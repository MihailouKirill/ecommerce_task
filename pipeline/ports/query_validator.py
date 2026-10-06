from abc import ABC, abstractmethod


class QueryValidatorPort(ABC):
    """
    Port for validating SQL queries before execution.
    """

    @abstractmethod
    def validate_query(self, query: str) -> str:
        """
        Validates and returns the cleaned SQL query.
        """
        pass
