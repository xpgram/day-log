from typing import Self
from abc import ABC, abstractmethod
from enums.View import View

class LogLine(ABC):
    "An abstract class describing an interface for log-related objects."

    @property
    @abstractmethod
    def logstreamType(self) -> str:
        pass

    @abstractmethod
    def __init__(self, data: str = None) -> Self:
        pass

    @abstractmethod
    def save(self) -> str:
        "Returns a comprehensive string for storing in the save file."
        pass

    @abstractmethod
    def render(self, view: View) -> str:
        "Returns a string for displaying in the terminal."
        pass
