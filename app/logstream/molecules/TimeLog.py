from app.logstream.molecules.LogstreamMolecule import LogstreamMolecule
from app.logstream.atoms.Time import Time
from app.logstream.atoms.Timecode import Timecode
from app.logstream.atoms.Category import Category
import app.system.Utils as Utils


class TimeLog(LogstreamMolecule):
  logstreamType = 'timelog-mol'

  timestamp: Time
  timecode: Timecode | None # TODO Optional? Or write a different class?
  category: Category

  @staticmethod
  def fromInput(data):
    time = Time.create(None)
    timecodeString, data = Utils.getToken(data)   # TODO And if tc doesn't exist?
    timecode = Timecode.create(timecodeString)
    category = Category.create(data)
    return TimeLog(time, timecode, category)
  
  @staticmethod
  def fromSave(data):
    timeStr, timecodeStr, categoryStr = data.split('#')
    return TimeLog(
      Time.create(timeStr),
      Timecode.create(timecodeStr),
      Category.create(categoryStr),
    )

  def __init__(self, time: Time, timecode: Timecode, category: Category):
    self.time = time
    self.timecode = timecode
    self.category = category

  def save(self):
    tokens = [
      self.time.save(),
      self.timecode.save(),
      self.category.save(),
    ]
    return '#'.join(tokens)
  
  def render(self, view):
    return f'{self.time.display()} {self.timecode.display()} {self.category.display()} --'
