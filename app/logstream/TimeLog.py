import app.system.Utils as Utils
from app.enums.TimecodeType import TimecodeType
from app.logstream.LogLine import LogLine

# TODO Lots of missing imports

class TimeLog(LogLine):
    "A logstream describing an event with a time window."
    logstreamType = 'time-log' # TODO What actually was my plan for these? Is this type checking?

    # TODO This either should be read in by __init__, or
    # TODO We expect the user to write '+2,1 money update - a note to append' and add the time ourselves.
    # Actually. This illuminates a point.
    # When loading from save, time is included. When creating a new, it isn't.
    # And also, I need [year, month, day, hour, minute]
    # TODO Time.py handles this.
    created = timeToString(datetime.now())
    timecode = ''
    timecodeType = TimecodeType.Time
    category = ''
    shortnote = '' # TODO Not shortnote, full note.
                   # Maybe excess after a '-' gets broken up into a separate logline.

    # TODO finish this, then test it out

    @staticmethod
    def fromInput(data: str):
        time = timeToString(datetime.now())
        data = f'{time} {data}'
        return TimeLog.fromSave(data)

    @staticmethod
    def fromSave(self, data: str = None):
        # TODO Load from data.
        # 22:37 +2,1 money update - a short note about what I did, or possibly a long one; somewhere else is supposed to enforce the length of these things.

        stream = data
        time, stream = Utils.getToken(stream)
        timecode, stream = Utils.getToken(stream)
        category, stream = Utils.getToken(stream)

        message = stream # TODO Send this to another logline?

        # TODO Anything goes wrong, throw a LogLine error
        # raise LogLineReadError('Hello.')

    def save(self) -> str: 
        tcTypePrefix = timecodeTypeToPrefix(self.timecodeType)
        shortnote = f' - {self.shortnote}' if len(self.shortnote) > 0 else ''
        return f'{self.created} {tcTypePrefix}{self.timecode or "0,0"} {self.category}{shortnote}'

    def render(self, view) -> str:
        content = f"{self.created} {self.timecode} {self.category} - {self.shortnote}"
        # TODO ' - ' removed when shortnote empty

        result = ''
        # TODO There has to be a better way of doing this.
        if view == View.Compact:
            result = content[:TERM_WIDTH]
        else:
            result = lineWrap(content, TERM_WIDTH, 2, 0)
        result = colorifyTimestamps(result)
        result = colorifyTimeCodes(result)
        return result
