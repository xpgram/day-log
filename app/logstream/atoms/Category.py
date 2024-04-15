import re
from app.system import Utils
from app.logstream.atoms.LogStreamAtom import LogStreamAtom
from app.enums.View import View
from app.logstream.Exceptions import LogstreamReadError

class Category(LogStreamAtom):
  logstreamType = 'category-atom'

  title: str
  subtitle: str

  @staticmethod
  def create(data):
    tokens = data.split(' - ')
    if not tokens[0]:
      raise LogstreamReadError(f'Category has no title.')
    if len(tokens) > 2:
      raise LogstreamReadError(f'Category has too many subheadings: "{data}"')
    
    title = tokens[0]
    subtitle = Utils.get(1, tokens, '')
    return Category(title, subtitle)
  
  def __init__(self, title: str, subtitle: str):
    self.title = title
    self.subtitle = subtitle

  def _getString(self):
    "Returns the base string for saves and renders to build from."
    separator = ' - ' if self.subtitle else ''
    return f'{self.title}{separator}{self.subtitle}'
  
  def save(self):
    return self._getString()

  def render(self, view):
    string = self._getString()
    if view == View.Compact:
      string = Utils.stringCutoff(string, 80)
    return string
