import re
import Utils
from logstream.Exceptions import LogstreamReadError
from logstream.atoms.LogStreamAtom import LogStreamAtom
from enums.TimecodeType import TimecodeType
from constants.TerminalColors import ColorCodes, TextModeCodes, wrapText

timecode_regex = r'^.?\d{1,2},\d$'

timecode_symbols = {
  '': TimecodeType.Time,
  '+': TimecodeType.Banked,
  '-': TimecodeType.Owed,
  '_': TimecodeType.Muted
}
timecode_symbols_inverse = Utils.inverseMap(timecode_symbols)

timecode_styles_map = {
  TimecodeType.Time: ColorCodes['Yellow'],
  TimecodeType.Banked: ColorCodes['Green'],
  TimecodeType.Owed: ColorCodes['Red'],
  TimecodeType.Muted: ColorCodes['DarkGray'],
}

class Timecode(LogStreamAtom):
  logstreamType = 'timecode-atom'

  timeType: TimecodeType
  hours = 0
  quarters = 0

  @staticmethod
  def create(data):
    if not re.match(timecode_regex, data):
      raise LogstreamReadError(f'Could not parse timecode "{data}"')

    [hours, quarters] = data.split(',')

    tcType = TimecodeType.Time
    if not hours[0].isdigit():
      symbol = hours[0]
      tcType = timecode_symbols.get(symbol, None)
      hours = hours[1:]

    if type(tcType) != TimecodeType:
      raise LogstreamReadError(f'Could not parse timecode type: "{data}"')
  
    return Timecode(tcType, hours, quarters)

  def __init__(self, timeType, hours, quarters):
    self.timeType = timeType
    self.hours = hours
    self.quarters = quarters

  def getString(self):
    tcSymbol = timecode_symbols_inverse.get(self.timeType)
    return f'{tcSymbol}{self.hours},{self.quarters}'

  def save(self):
    return self.getString()

  def render(self, view):
    return wrapText(
      timecode_styles_map[self.timeType],
      self.getString()
    )
