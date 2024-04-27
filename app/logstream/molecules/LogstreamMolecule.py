
"""
# TODO 
[x] Built in save, render, display as from Atom.
[x] Built in line wrapping. Or full width stringCutoff in compact mode.
 -  May have many atom components. Or just one.
[ ] Built in indenting for UI things like line numbers.
"""

from typing import Self
from abc import ABC, abstractmethod
from datetime import datetime
import textwrap
from app.system.Utils import Utils
import app.constants.Viewport as Viewport
from app.enums.View import View
from app.state.ViewState import ViewState

class LogstreamMolecule(ABC):
  "An abstract class describing an interface for log-related atoms."

  # TODO Line number memory is held here (?)
  _lineNumber = '1'

  _createdOn = datetime.now()

  _renderCache: str | None = None


  @property
  @abstractmethod
  def logstreamType(self) -> str:
    "The.. class of object this is?" # TODO Answer this question.


  @staticmethod
  @abstractmethod
  def fromInput(data: str) -> Self:
    "Construct a new Logstream object from user input."

  @staticmethod
  @abstractmethod
  def fromSave(data: str) -> Self:
    "Construct a new Logstream object from save data."

  @abstractmethod
  def save(self) -> str:
    "Returns a comprehensive string for storing in the save file."
    # TODO This should include the ls-type for easy read back. Is that why I wrote them?

  @abstractmethod
  def render(self, view: View) -> str:
    "Returns a render string built according to the given View type."

  # TODO These two functions are supposed to support the inheritor's own save and load methods.
  # I'm not sure... if I like this idea, though.
  # 
  # I've been trying (_trying_) to maintain a readable plain text file as the 'save' for this app,
  # but maybe that's not realistic. Maybe I do need to think about json or sqlite.
  def getStandardDataSaveString(self) -> str:
    ""
    return self._createdOn.strftime('%H:%M')

  def loadStandardDataSaveString(self, data: str):
    ""
    # TODO Data is assumed to be much more than the tokens this abstract will itself save.
    # So... We could use another delimiter. A super delimiter.
    # This would be a lot easier with an segmentable dictionary. Like:
    #   data['logstream'], and data['timelog']

    createdOnStr, data = Utils.getToken(data, '#') # TODO Is this correct? I forget.
    self._createdOn = datetime.strptime(createdOnStr, '%H:%M') # TODO The condensed format is time only, but that requires cooperation among the logstream.

  def cacheRender(self, view: View):
    "Renders and caches the display string."
    displayString = self.render(view)

    displaySwitch = {
      View.Compact: self._compactDisplay,
      View.Markdown: self._markdownDisplay,
    }
    displayMethod = displaySwitch.get(ViewState.get(), self._normalDisplay)

    self._renderCache = displayMethod(displayString)

  def display(self) -> str:
    "Returns a string to display in the terminal."
    if not self._renderCache:
      self.cacheRender(ViewState.get())
    return self._renderCache

  def _renderIndents(self):
    ""
    initialIndent = ''
    subsequentIndent = ' '*3
    return initialIndent, subsequentIndent

  def _normalDisplay(self, displayString):
    initialIndent, subsequentIndent = self._renderIndents()
    # if useLineNumbers:    # TODO
    #   initialIndent = f'{self._lineNumber:0>2} {initialIndent}'
    #   subsequentIndent = f'-- {subsequentIndent}'

    # Preserve '\n' characters, which textwrap will strip.
    paragraphs = displayString.split('\n')

    # Textwrap and format each paragraph
    for idx in range(0, len(paragraphs)):
      lines: list[str]
      paragraph = paragraphs[idx]

      if idx == 0:
        lines = textwrap.wrap(
          text = paragraph,
          width = Viewport.TermWidth,
          initial_indent= initialIndent,
          subsequent_indent = subsequentIndent,
        )
      else:
        lines = textwrap.wrap(
          text = paragraph,
          width = Viewport.TermWidth,
          initial_indent= subsequentIndent,
          subsequent_indent = subsequentIndent,
        )
      # Rejoin textwrapped lines
      paragraph = '\n'.join(lines)
      paragraphs[idx] = paragraph

    # Rejoin split '\n' characters
    return '\n'.join(paragraphs)

  def _compactDisplay(self, displayString):
    prefix = ''
    # if useLineNumbers:    # TODO
    #   prefix = f'{self.lineNumber:0>2} '
    return prefix + Utils.stringCutoff(displayString, Viewport.TermWidth)

  def _markdownDisplay(self, displayString):
    # No line numbers
    return displayString
