from datetime import datetime
from logstream.atoms.LogStreamAtom import LogStreamAtom
from logstream.Exceptions import LogstreamReadError

datetime_save_format = '%Y %m %d %H:%M'
timestamp_regex = r'^\d{4} \d{2} \d{2} \d{2}:\d{2}$'

class Time(LogStreamAtom):
  logstreamType = 'time-atom'

  date: datetime

  @staticmethod
  def create(data):
    try:
      date = datetime.strptime(data, datetime_save_format) if data else datetime.now()
      return Time(date)
    except ValueError:
      raise LogstreamReadError(f'Could not parse date: "{data}"')

  def __init__(self, date: datetime):
    self.date = date

  def save(self):
    return self.date.strftime(datetime_save_format)

  def render(self, view):
    from constants.TerminalColors import TextColor, wrapText
    return wrapText(
      TextColor['Cyan'],
      self.date.strftime('%H:%M')
    )
