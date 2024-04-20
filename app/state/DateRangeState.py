from app.system import Dispatcher
from app.constants import Events
from datetime import datetime

# TODO Should this be in a different file?
class DateRange:
  start: datetime | None
  end: datetime | None

  def __init__(self, start: datetime, end: datetime = None):
    self.start = start
    self.end = end


_dateRange = DateRange()

class DateRangeState:
  @staticmethod
  def get() -> DateRange:
    "Returns the current DateRange state."
    return _dateRange

  @staticmethod
  def set(range: DateRange):
    "Sets the current DateRange state and emits this as an event."
    global _dateRange
    _dateRange = range
    DateRangeState.announce()

  @staticmethod
  def announce():
    "Emits a global event carrying the current DateRange state as data."
    Dispatcher.emit(Events.ViewStateUpdated, _dateRange)
