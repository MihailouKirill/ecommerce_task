from abc import ABC, abstractmethod


class ITransformerPort[T](ABC):
    """
    Port for data transformation operations.
    """

    @abstractmethod
    def __call__(self, data: T) -> T:
        """
        Applies transformation logic to the given DataFrame.
        """
