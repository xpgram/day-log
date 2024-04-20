from app.logstream.molecules.LogstreamMolecule import LogstreamMolecule
from app.enums.View import View


class NoteLog(LogstreamMolecule):
  logstreamType = 'notelog-mol'

  text: str

  @staticmethod
  def fromInput(data):
    return NoteLog(data)
  
  @staticmethod
  def fromSave(data):
    return NoteLog(data)

  def __init__(self, text: str):
    self.text = text

  def save(self):
    return self.text
  
  def render(self, view):
    if view == View.Compact:
      return ''
    return f' - {self.text}'
