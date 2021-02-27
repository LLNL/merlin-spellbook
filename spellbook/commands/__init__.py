from abc import ABC, abstractmethod


class CliCommand(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError()
