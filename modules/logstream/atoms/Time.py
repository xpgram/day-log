
"""
This atom is for this part.
|---|
12:31 +2,1 cras pulvinar - Mattis nunc sed blandit libero volutpat sed cras quis
"""

from logstream.atoms.LogStreamAtom import LogStreamAtom

class Time(LogStreamAtom):
  logstreamType = 'time-atom'

  @staticmethod
  def create(data):
    pass

  def save():
    pass

  def render(self, view):
    pass
