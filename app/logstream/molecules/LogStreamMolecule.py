
"""
# TODO 
[x] Built in save, render, display as from Atom.
[x] Built in line wrapping. Or full width stringCutoff in compact mode.
 -  May have many atom components. Or just one.
[ ] Built in indenting for UI things like line numbers.
"""

import app.system.Utils as Utils
import textwrap
from typing import Self
from abc import ABC, abstractmethod
import app.constants.Viewport as Viewport
from app.enums.View import View
from app.state.ViewState import ViewState

class LogstreamMolecule(ABC):
  "An abstract class describing an interface for log-related atoms."

  # TODO Line number memory is held here (?)
  _lineNumber = '1'

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

    displaySwitch = {
      View.Compact: self.compactDisplay,
      View.Markdown: self.markdownDisplay,
    }
    displayMethod = displaySwitch.get(ViewState.get(), self.normalDisplay)

    return displayMethod()

  def normalDisplay(self):
    initialIndent = ''
    subsequentIndent = ' '*3
    # if useLineNumbers:    # TODO
    #   initialIndent = f'{self._lineNumber:0>2} '
    #   subsequentIndent = '-- ' + ' '*3

    lines = textwrap.wrap(
      text = self._renderCache,
      width = Viewport.TermWidth,
      initial_indent= '',
      subsequent_indent = ' '*3,
    )
    return '\n'.join(lines)

  def compactDisplay(self):
    prefix = ''
    # if useLineNumbers:    # TODO
    #   prefix = f'{self.lineNumber:0>2} '
    return prefix + Utils.stringCutoff(self._renderCache, Viewport.TermWidth)

  def markdownDisplay(self):
    # No line numbers
    return self._renderCache
