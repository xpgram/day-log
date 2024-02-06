from typing import Self
from abc import ABC, abstractmethod

class LogLine(ABC):
    "An abstract class describing an interface for log-related objects."

    @property
    @abstractmethod
    def lstype(self) -> str:
        pass

    @abstractmethod
    def __init__(self, data: str = None) -> Self:
        pass

    @abstractmethod
    def save(self) -> str:
        "Returns a comprehensive string for storing in the save file."
        pass

    @abstractmethod
    def render(self, view: View) -> str:    # TODO Missing import
        "Returns a string for displaying in the terminal."
        pass
