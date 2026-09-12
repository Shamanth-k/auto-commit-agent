from abc import ABC, abstractmethod


class BaseExecutor(ABC):

    @abstractmethod
    def execute(self, task: dict, repository_path: str) -> None:
        pass