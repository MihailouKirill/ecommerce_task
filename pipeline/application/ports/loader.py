from abc import ABC, abstractmethod


class ILoaderPort[T](ABC):
    """
    Port for data loading operations.
    """

    @abstractmethod
    def load(self, data: T) -> None:
        """
        Saves the final DataFrame.

        Args:
            data:Processed DataFrame to save.
        """
