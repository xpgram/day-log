from app.logstream.atoms.LogStreamAtom import LogStreamAtom
from app.enums.View import View

class Category(LogStreamAtom):
  logstreamType = 'category-atom'

  title: str
  subtitle: str # TODO `adminia - firefox tweaks - [a message about what I spent my t...]`
                # Should I bother with this? Sometimes I do this.

  @staticmethod
  def create(data):
    return Category(data)
  
  def __init__(self, title: str):
    self.title = title

  def save(self):
    return self.title

  def render(self, view):
    if view == View.Compact:
      return self.title[:12]  # TODO ??
    return self.title

