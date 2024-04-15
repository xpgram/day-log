from math import trunc
import re
import app.system.Utils as Utils
from app.logstream.Exceptions import LogstreamReadError
from app.logstream.atoms.LogStreamAtom import LogStreamAtom
from app.enums.TimecodeType import TimecodeType
from app.constants.TerminalColors import TextColor, wrapText

SUBHOUR_CHUNKS = 4

timecode_regex = r'^.?\d{1,2},\d$'

timecode_symbols = {
  '': TimecodeType.Time,
  '+': TimecodeType.Banked,
  '-': TimecodeType.Owed,
  '_': TimecodeType.Muted
}
timecode_symbols_inverse = Utils.inverseMap(timecode_symbols)

timecode_styles_map = {
  TimecodeType.Time: TextColor['Yellow'],
  TimecodeType.Banked: TextColor['Green'],
  TimecodeType.Owed: TextColor['Red'],
  TimecodeType.Muted: TextColor['DarkGray'],
}

class Timecode(LogStreamAtom):
  logstreamType = 'timecode-atom'

  timeType: TimecodeType
  hours = 0
  subhours = 0

  @staticmethod
  def create(data):
    if not re.match(timecode_regex, data):
      raise LogstreamReadError(f'Could not parse timecode "{data}"')

    [hours, subhours] = data.split(',')

    tcType = TimecodeType.Time
    if not hours[0].isdigit():
      symbol = hours[0]
      tcType = timecode_symbols.get(symbol, None)
      hours = hours[1:]

    hours = int(hours)
    subhours = int(subhours)

    if subhours / SUBHOUR_CHUNKS >= 1:
      hours += trunc(subhours / SUBHOUR_CHUNKS)
      subhours = subhours % SUBHOUR_CHUNKS

    if type(tcType) != TimecodeType:
      raise LogstreamReadError(f'Could not parse timecode type: "{data}"')
  
    return Timecode(tcType, hours, subhours)

  def __init__(self, timeType: TimecodeType, hours: int, subhours: int):
    self.timeType = timeType
    self.hours = hours
    self.subhours = subhours

  def _getString(self):
    tcSymbol = timecode_symbols_inverse.get(self.timeType)
    return f'{tcSymbol}{self.hours},{self.subhours}'

  def save(self):
    return self._getString()

  def render(self, view):
    return wrapText(
      timecode_styles_map[self.timeType],
      self._getString()
    )
