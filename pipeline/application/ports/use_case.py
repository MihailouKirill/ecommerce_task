"""
Use case port contract for the application layer.
"""

from abc import ABC, abstractmethod


class IUseCasePort(ABC):
    """
    Primary port interface for application use cases.
    """

    @abstractmethod
    def execute(self) -> None:
        """
        Executes the business logic of the use case.
        """
