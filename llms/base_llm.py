from abc import ABC, abstractmethod


class BaseLLM(ABC):
    @abstractmethod
    def make_request(self):
        pass
