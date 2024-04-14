
"""
This atom is for this part.
|---|
12:31 +2,1 cras pulvinar - Mattis nunc sed blandit libero volutpat sed cras quis
"""

from datetime import datetime
from logstream.atoms.LogStreamAtom import LogStreamAtom

class Time(LogStreamAtom):
  logstreamType = 'time-atom'

  date: datetime

  @staticmethod
  def create(data):
    # TODO Read from data
    date = datetime.now()
    return Time(date)

  def __init__(self, date: datetime):
    self.date = date

  def save(self):
    return self.date.strftime('%Y %m %d %H:%M')

  def render(self, view):
    return self.date.strftime('%H:%M')
