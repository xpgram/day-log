from app.logstream.molecules.LogstreamMolecule import LogstreamMolecule
from app.logstream.atoms.Time import Time
from app.logstream.atoms.Timecode import Timecode
from app.logstream.atoms.Category import Category
from app.system.Utils import Utils


class TimeLog(LogstreamMolecule):
  logstreamType = 'timelog-mol'

  timestamp: Time
  timecode: Timecode | None # TODO Optional? Or write a different class?
  category: Category

  # TODO shortnote is allowable, but it should be length-limited; i.e. _short_.
  shortnote: str

  @staticmethod
  def fromInput(data):
    time = Time.create(None)

    timecodeString, data = Utils.getToken(data)   # TODO And if tc doesn't exist?
    category, shortnote = Utils.getToken(data, ' -- ')

    timecode = Timecode.create(timecodeString)
    category = Category.create(category)
    shortnote = shortnote or ''
    return TimeLog(time, timecode, category, shortnote)
  
  @staticmethod
  def fromSave(data):
    timeStr, timecodeStr, categoryStr, shortnote = data.split('#')
    return TimeLog(
      Time.create(timeStr),
      Timecode.create(timecodeStr),
      Category.create(categoryStr),
      shortnote
    )

  def __init__(self, time: Time, timecode: Timecode, category: Category, shortnote: str):
    self.time = time
    self.timecode = timecode
    self.category = category
    self.shortnote = shortnote

  def save(self):
    tokens = [
      self.time.save(),
      self.timecode.save(),
      self.category.save(),
      self.shortnote
    ]
    return '#'.join(tokens)
  
  def render(self, view):
    shortnoteSeparator = ' -- ' if len(self.shortnote) > 0 else ''
    return f'{self.time.display()} {self.timecode.display()} {self.category.display()}{shortnoteSeparator}{self.shortnote}'
