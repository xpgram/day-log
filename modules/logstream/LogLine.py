from typing import Self
from abc import ABC, abstractmethod
from enums.View import View

class LogLineReadError(Exception):
    """An exception for LogLine input stream errors."""

class LogLine(ABC):
    "An abstract class describing an interface for log-related objects."

    @property
    @abstractmethod
    def logstreamType(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def fromInput(data: str) -> Self:
        pass

    @staticmethod
    @abstractmethod
    def fromSave(data: str) -> Self:
        pass

    @abstractmethod
    def save(self) -> str:
        "Returns a comprehensive string for storing in the save file."
        pass

    @abstractmethod
    def render(self, view: View) -> str:
        "Returns a string for displaying in the terminal."
        pass
