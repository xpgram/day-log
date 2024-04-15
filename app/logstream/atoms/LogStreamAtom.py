from typing import Self
from abc import ABC, abstractmethod
from app.enums.View import View
from app.state.ViewState import ViewState

class LogStreamAtom(ABC):
    "An abstract class describing an interface for log-related atoms."

    @property
    @abstractmethod
    def logstreamType(self) -> str:
        "The.. class of object this is?" # TODO Answer this question.

    @staticmethod
    @abstractmethod
    def create(data: str | None) -> Self:
        "Assembles a new object of this class."

    @abstractmethod
    def save(self) -> str:
        "Returns a comprehensive string snippet for storing in the save file."

    @abstractmethod
    def render(self, view: View) -> str:
        "Returns a render string built according to the given View type."

    _renderCache: str | None = None

    def cacheRender(self, view: View):
        "Renders and caches the display string."
        self._renderCache = self.render(view)

    def display(self) -> str:
        "Returns a string snippet for displaying somewhere in the terminal."
        if not self._renderCache:
            self.cacheRender(ViewState.get())
        return self._renderCache
