from abc import ABC, abstractmethod


class IQueryValidatorPort(ABC):
    """
    Port for validating SQL queries before execution.
    """

    @staticmethod
    @abstractmethod
    def validate_query(query: str) -> str:
        """
        Validates and returns the cleaned SQL query.
        """
