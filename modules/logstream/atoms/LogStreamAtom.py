from typing import Self
from abc import ABC, abstractmethod
from enums.View import View

class LogLine(ABC):
    "An abstract class describing an interface for log-related atoms."

    @property
    @abstractmethod
    def logstreamType(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def create(data: str | None) -> Self:
        pass

    @abstractmethod
    def save(self) -> str:
        "Returns a comprehensive string snippet for storing in the save file."
        pass

    @abstractmethod
    def render(self, view: View) -> str:
        "Returns a string snippet for displaying in the terminal."
        pass
