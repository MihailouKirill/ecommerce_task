from abc import ABC, abstractmethod


class ICompactorPort(ABC):
    """
    Port for consolidating and compacting report files.
    """

    @abstractmethod
    def compact(self) -> None:
        """Consolidates accumulated raw report files."""
