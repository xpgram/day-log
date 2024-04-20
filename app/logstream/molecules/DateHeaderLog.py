from datetime import datetime, timedelta
from app.logstream.molecules.LogstreamMolecule import LogstreamMolecule
from app.enums.View import View
from app.constants.TerminalColors import TextColor, wrapText
from app.logstream.Exceptions import LogstreamInputError, LogstreamReadError
from app.system.Utils import Utils

datetime_save_format = '%A %B %d, %Y'

# TODO [ ] Logstream considers LogLines as owned by a dateHeader farther back in time.
# TODO [ ] `print date apr 21` finds the DateHeader for April 21 [this year] and prints
#    all logstream objects after it until discovering the next DateHeader object.
# TODO [ ] DateHeaders are mapped by date to indices in the stream, for quick retrieval.

class DateHeaderLog(LogstreamMolecule):
  logstreamType = 'dateheader-mol'

  date: datetime

  @staticmethod
  def fromInput(data):
    inputDays = Utils.stringToInt(data) if data and len(data) > 0 else 0

    if type(inputDays) != int:
      raise LogstreamInputError(f'Could not parse date header adjustment: "{data}"; should be a +/- integer.')

    daysAdjustment = timedelta(days = inputDays)
    date = datetime.now() + daysAdjustment
    return DateHeaderLog(date)
  
  @staticmethod
  def fromSave(data):
    try:
      date = datetime.strptime(data, datetime_save_format)
    except ValueError as err:
      raise LogstreamReadError(f'Could not parse date object: "{err}"')

    return DateHeaderLog(date)

  def __init__(self, date: datetime):
    self.date = date

  def save(self):
    return self.date.strftime(datetime_save_format)
  
  def render(self, view):
    dateString = self.date.strftime(datetime_save_format)
    if (view != View.Markdown):
      dateString = wrapText(TextColor['DarkGray'], dateString)
    return f'\n{dateString}'
  
  def _renderIndents(self):
    initialIndent = ''
    subsequentIndent = ''
    return initialIndent, subsequentIndent
