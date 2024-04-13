from typing import Self
from abc import ABC, abstractmethod
from enums.View import View
from state import ViewState

class LogLine(ABC):
    "An abstract class describing an interface for log-related objects."

    @property
    @abstractmethod
    def logstreamType(self) -> str:
        "The.. class of object this is?" # TODO Answer this question.

    @staticmethod
    @abstractmethod
    def fromInput(data: str) -> Self:
        "Construct a new LogStream object from user input."

    @staticmethod
    @abstractmethod
    def fromSave(data: str) -> Self:
        "Construct a new LogStream object from save data."

    @abstractmethod
    def save(self) -> str:
        "Returns a comprehensive string for storing in the save file."

    @abstractmethod
    def render(self, view: View) -> str:
        "Returns a render string built according to the given View type."

    _renderCache: str | None = None

    def cacheRender(self, view: View) -> str:
        "Renders and caches the display string."
        self._renderCache = self.render(view)

    def display(self) -> str:
        "Returns a string to display in the terminal."
        if not self._renderCache:
            self.cacheRender(ViewState.get())
        return self._renderCache
        
