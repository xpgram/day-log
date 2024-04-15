
"""
# TODO 
[x] Built in save, render, display as from Atom.
[ ] Built in line wrapping. Or full width stringCutoff in compact mode.
[ ] May have many atom components. Or just one.
[ ] Built in indenting for UI things like line numbers.
"""

from typing import Self
from abc import ABC, abstractmethod
from app.enums.View import View
from app.state.ViewState import ViewState

class LogstreamMolecule(ABC):
    "An abstract class describing an interface for log-related atoms."

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
        # TODO This should include the ls-type for easy read back. Is that why I wrote them?

    @abstractmethod
    def render(self, view: View) -> str:
        "Returns a render string built according to the given View type."

    _renderCache: str | None = None

    def cacheRender(self, view: View):
        "Renders and caches the display string."
        self._renderCache = self.render(view)

    def display(self) -> str:
        "Returns a string to display in the terminal."
        if not self._renderCache:
            self.cacheRender(ViewState.get())
        return self._renderCache

