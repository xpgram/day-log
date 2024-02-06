from LogLine import LogLine

# TODO Lots of missing imports

class TimeLog(LogLine):
    "A logstream describing an event with a time window."
    lstype = 'tlog'

    created = timeToString(datetime.now())
    timecode = ''
    timecodeType = TimecodeType.Time
    category = ''
    shortnote = ''

    # TODO finish this, then test it out

    def __init__(self, data: str = None):
        if data == None:
            return
        
        # TODO Load from data.
        # 22:37 +2,1 money update - a short note about what I did, or possibly a long one; somewhere else is supposed to enforce the length of these things.

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
