from abc import ABC, abstractmethod


class UseCasePort(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
