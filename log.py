from typing import Sequence, TypeVar, Callable, Optional, Self

from datetime import date, datetime, time
import platform
import subprocess
import textwrap
import shlex
import json
import os
import sys
import re

T = TypeVar('T')

# TODO Is textwrap core?



####################################################################################################
#### Support functions                                                                          ####
####################################################################################################

####################################################################################################
#### String convenience functions

class String:

    @staticmethod
    def insert(idx: int, substr: str, target: str):
        "Returns a new string copy of 'target' with 'substr' inserted into it at position 'idx'."
        leftHalf = target[:idx]
        rightHalf = target[idx:]
        return f"{leftHalf}{substr}{rightHalf}"


####################################################################################################
#### Regex strings and checkers

# Regex patterns
regexPattern = {
    'timestamp': r'\d{1,2}:\d{2}',                              # timestamp (17:13)
    'timecode': r'[_\+-=]?\d{1,2},\d',                          # timecode (1,1)
    'date': r'^[a-zA-Z]{3} [0123]?\d(, (\d{2}|\d{4}))?$',       # normal format date (Jan 02, 2020)
    'dateShort': r'^[01]?\d-[0123]?\d(-(\d{2}|\d{4}))?$',       # short format date (1-2-20)
}

def regexCheck(pattern, string):
    "Returns True if the given string matches the given regex pattern."
    return re.search(pattern, string)


####################################################################################################
#### Color code regex functions

def colorifyTimestamps(s: str):
    ""
    timestamps_iter = re.finditer(regexPattern['timestamp'], s)
    timestamps = [ ts for ts in timestamps_iter ]
    result = s[:]

    # Iterate in reversed order so the math of inserting sub-strings is easier.
    for timestamp in reversed(timestamps):
        result = String.insert(timestamp.end(), Color['NoColor'], result)
        result = String.insert(timestamp.start(), Color['Cyan'], result)

    return result


def colorifyTimeCodes(s: str):
    ""
    colorMap = {
        TimecodeType.Time: Color['Orange'],
        TimecodeType.Banked: Color['Green'],
        TimecodeType.Owed: Color['Red'],
        TimecodeType.Muted: Color['DarkGray'],
    }

    timecodes_iter = re.finditer(regexPattern['timecode'], s)
    timecodes = [ tc for tc in timecodes_iter ]
    result = s[:]

    # Iterate in reversed order so color codes can be added to the result string without complex math.
    for code in reversed(timecodes):
        prefix = code.group()[0]
        tcType = timecodePrefixToType(prefix)
        colorMode = colorMap.get(tcType, '')
        colorReset = Color['NoColor']

        result = String.insert(code.end(), colorReset, result)
        result = String.insert(code.start(), colorMode, result)

    return result


####################################################################################################
#### Date / Time functions

def dateToString(d: date) -> str:
    "Converts a date object to a formatted date string."
    return d.strftime('%a %b %d, %Y')

def dateFromString(s: str) -> date:
    "Converts a formatted date string to a date object."
    return datetime.strptime(s, '%a %b %d, %Y').date()

def parseDate(s: str) -> date | None:
    "Returns a date object parsed from a string s, or returns None if one couldn't be interpreted."
    result = None
    datePatterns = (
        '%b %d, %Y',
        '%b %d',
        '%Y-%m-%d',
        '%m-%d-%y',
        '%m-%d-%Y',
        '%m-%d'
        )
    for pattern in datePatterns:
        try:
            result = datetime.strptime(s, pattern).date()
            break
        except ValueError:
            pass
    if result != None:
        if result.year == 1900:     # Just assume a year wasn't provided; I got no relationship with 1900
            result = result.replace(year=date.today().year)
    return result

def timeToString(d: time) -> str:
    "Converts a date object to a formatted timestamp string."
    return d.strftime('%H:%M')

def timeFromString(s: str) -> time:
    "Converts a formatted timestamp string to a date object."
    return datetime.strptime(s, '%H:%M').time()

def parseTime(s: str) -> time | None:
    "Returns a time object parsed from a string s, or returns None if one couldn't be interpreted."
    result = None
    timePatterns = (
        '%H:%M',
        '%H%M',
        )
    for pattern in timePatterns:
        try:
            result = datetime.strptime(s, pattern).time()
            break
        except ValueError:
            pass
    return result


####################################################################################################
#### Timecode Functions

TimecodeConversionMap = {
    TimecodeType.Time: '',
    TimecodeType.Banked: '+',
    TimecodeType.Owed: '-',
    TimecodeType.Muted: '_',
}

def timecodeTypeToPrefix(tctype: TimecodeType) -> str:
    return TimecodeConversionMap.get(tctype, TimecodeType.Time)

def timecodePrefixToType(prefix: str) -> TimecodeType:
    for key in TimecodeConversionMap:
        if TimecodeConversionMap[key] == prefix:
            return key
    return TimecodeType.Time


####################################################################################################
#### Print functions                                                                            ####
####################################################################################################

displayString = []

def printBuffer(message=''):
    "'Prints' to an internal buffer string."
    displayString.append(message)

def displayBuffer():
    "Prints the internal buffer string to the console, then resets the buffer."
    global displayString
    if len(displayString) > 0:
        # TODO This will probably need adjusting with the new print stuff. Or possibly merging.
        content = '\n'.join(displayString)
        print(f'\n{content}\n')
    displayString = []

def lineWrap(message: str, width= 98, indent= 0, initialIndent= None):
    "Wraps the given message to some character width limit, including a left-margin equal to indent."
    if initialIndent == None:
        initialIndent = indent
    indent = ' ' * indent
    initialIndent = ' ' * initialIndent

    newLines = textwrap.wrap(
        text= message,
        width= width,
        initial_indent= initialIndent,
        subsequent_indent= indent,
        )
    return '\n'.join(newLines)


####################################################################################################
#### Terminal Reprint functions

# TODO Does this work in windows? Do I need OS detection + an equivalent?
# I tried TermLinuxCore and TermWindowsCore, but it lacked yellow functions.
# I don't know how to convert Term to Windows yet.
# TODO Also, I wanted to see if I could edit the terminal screen while input() is active.
# Without any fuckups, I mean.
# I might still have the code for testing in TestB
class Term:
    def print(text):
        print(text)

    def moveTo(line, column):
        subprocess.run(['tput', 'cup', str(line), str(column)])

    def moveUp(lines =1):
        subprocess.run(['tput', 'cuu', str(lines)])

    def moveDown(lines =1):
        subprocess.run(['tput', 'cud', str(lines)])

    def saveCursor():
        subprocess.run(['tput', 'sc'])

    def restoreCursor():
        subprocess.run(['tput', 'rc'])

    def clearLine():
        "Clears all characters on the row the cursor is located."
        # TODO Does 'el' work like that? Or do I need extra instructions?
        subprocess.run(['tput', 'el'])

    def clearDown():
        "Clears all characters on all rows below the one the cursor is located."
        subprocess.run(['tput', 'cd'])

    def clearScreen():
        "Clears all characters."
        subprocess.run('clear')

    # TODO The model I want is probably a coordinate display, not relative.
    #  So, we'd decide only 40 rows are necessary, and row 2 is the 2nd from the top, etc.
    def replaceLine(reverseIndex, text):
        "Replaces text on a row above the cursor without displacing the cursor."
        Term.saveCursor()
        Term.moveUp(reverseIndex)
        Term.clearLine()
        Term.print(text)
        Term.restoreCursor()


####################################################################################################
#### Logstream Objects                                                                          ####
####################################################################################################


class DateHeader(LogLine):
    "A logstream describing a date."
    lstype = 'date'

    date = dateToString(date.today())

    def __init__(self, data: str = None):
        self.date = dateToString(parseDate(data))

    def save(self) -> str:
        return self.date

    def render(self, view) -> str:
        return f"\n{Color['DarkGray']}{self.date}{Color['NoColor']}"


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


class LogNote(LogLine):
    "A logstream describing a note appended to a timestamped logstream event."
    lstype = 'note'

    bullet = False
    text = ''

    def __init__(self, data: str = None):
        if data == None:
            return

        self.bullet = (data[0] == '-')
        self.text = data if not self.bullet else data[1:].strip()

    def save(self) -> str:
        prefix = '- ' if self.bullet else ''
        return f'{prefix}{self.text}'

    def render(self, view) -> str:
        if view == View.Compact:
            return ''

        bulletPrefix = '- ' if self.bullet else ''
        content = f"{bulletPrefix}{self.text}"
        firstlineIndent = 1 if self.bullet else 3
        
        result = lineWrap(content, TERM_WIDTH, 2, firstlineIndent)
        result = colorifyTimeCodes(result)
        return result

class LogStream:
    ""
    view: View = View.Normal
    stream: list[LogLine] = []

    showLineNumbers = False # TODO Is this a setting or a View?

    def __init__(self, logfile = None):
        if logfile != None:
            self.read(logfile)

    def read(self, logfile):
        ""
        # TODO Load data from logfile.
        pass

    def save(self) -> str:
        ""
        # TODO This is a save-all operation. Is that really necessary? Can we not save only the lines that are new?
        savedStrings = [ log.save() for log in self.stream ]
        return '\n'.join(savedStrings)

    def render(self) -> str:
        ""
        curLineNumber = len(self.stream) # TODO This is supposed to be relative to your view.
        renderStrings: list[str] = []

        for log in self.stream:
            curLineNumber -= 1
            renderString = log.render(self.view)
            if renderString == '':  # TODO Should this be None instead?
                continue
            
            if self.showLineNumbers:
                renderString = f'{curLineNumber:0>2}  {renderString}'

            renderStrings.append(renderString)

        return '\n'.join(renderStrings)


####################################################################################################
#### ID Managing Functions                                                                      ####
####################################################################################################

def newID(file, l=4):
    "I don't know if this will be used yet."
    return '1' # Return the date, I guess? That's guaranteed to be unique. Sorta.


####################################################################################################
#### Argument Processor Functions                                                               ####
####################################################################################################

class InputProcessorState:
    "Represents the input-looper's state at any one instant."

    def __init__(self, logstream, args, commandSet):
        self.logstream = logstream          # The current app-state; allows commands to modify the app-state.
        self.args = args                    # The remaining arguments to the script that need to be parsed over.
        self.commandSet = commandSet        # The commands available to the script in this processor state.

        # Other properties
        self.lastArg = None                 # The last arg seen by this state. Represents current - 1.
        self.pollingEnabled = True          # Whether this proc-state desires user input to fill its argument queue.
        
    def shift(self):
        "Returns the next script argument."
        self.last, self.args = shift(self.args)
        return self.last
    
    def unshift(self):
        "Replaces the last shifted script argument into the args queue."
        if self.last != None:
            self.args = [self.last] + self.args
            self.last = None

    def lookahead(self, i: int):
        "Returns the i-th argument from the remaining args."
        return get(i, self.args)
    
    def clear(self):
        "Empties the args queue."
        self.args = []
        self.last = None

# TODO This needs reformulating. There is no script input. You just run it.
def inputProcessor(state: InputProcessorState):
    "The 'game loop', if you will."

    # A do-until construction.
    while True:
        # TODO loop
        # print logstream in whichever view
        # print metadata about log: message, time total, bank
        # prompt line
        #   input is sent to input-proc
        #   input-proc returns new state (and modifies log file?)
        #   commands like /exit have some way of communicating 'leave the app'
        
        # Execute command instruction and collect new state for next iteration.
        command = state.shift()
        state = state.commandSet.switch(command)(state)
        assert type(state) == InputProcessorState, 'All input processor functions must return an input processor state.'

        # until clause
        if not (state.args or state.pollingRequested()):
            break




# TODO This looks good. Nice.
logstream = LogStream()

# ================
datehead = DateHeader('Jan 13, 2023')
logstream.stream.append(datehead)

# ================
tlog = TimeLog()
tlog.category = 'money update'
tlog.shortnote = 'forgot to remove in-source todo comments'
tlog.timecode = '0,1'
logstream.stream.append(tlog)

note1 = LogNote('- Oh, an fixed some typos.')
logstream.stream.append(note1)

# ================
tlog = TimeLog()
tlog.category = 'money update'
tlog.shortnote = 'fixed the thing about the thing with the thing that needed more stuff from the thing. now it works just fine.'
tlog.timecode = '2,1'
logstream.stream.append(tlog)

note1 = LogNote('- how are you going to do anything now? what if grandpa finds out? I don\'t have the answers to these questions, but I may know who does.')
logstream.stream.append(note1)

note2 = LogNote('oh, actually, grandpa does know.')
logstream.stream.append(note2)

# ================
logstream.view = View.Normal
r = logstream.render()
print(r)



''' Screen mock up
10  Tue Jan 15, 2023
09  17:15 1,2 money update
08  - Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt
08   ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
08   laboris nisi ut aliquip ex ea commodo consequat.
07    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt
07   ut labore et dolore magna aliqua.
06  - Lorem ipsum dolor sit amet, consectetur adipiscing elit.
05
05  Wed Jan 16, 2023
04  09:00 0,2 money update
03   - Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt
03    ut labore et dolore magna aliqua.
02   - Ut enim ad minim veniam, quis nostrud exercitation ullamco.
02     Laboris nisi ut aliquip ex ea commodo consequat.
01  09:45 0,3 money update
00   - Finally fixed the thing. So cool.
[                                                       : Today 1,1  Bank 11,2 ]   Status bar. Prints messages to user.

'''

'''
        Add line to previous log note.
-       New log note, appended to previous timelog.
:       New timelog, autoset the timecode. Will merge into last if they round to the same div-15.
: 0,2   New timelog, set the timecode to '0,2'. This will never merge.
:: 0,2  New timelog, extend from the previous one. Will fail w/o a timecode. Use this if it's been 0,3 and you need to log a 0,1 then a 0,2.
: --    New timelog, no timecode. Useful for timestamped notes. Does not contribute to hourly totals.
<       Undo previous line. May be multi-line if it extends past the linewrap. Adds the removed line (instruction?) to clipboard.
>       Redo an undo? Probably 're-adds a line', which is slightly different. You could undo, submit, redo to insert something.

Ex:
: 0,2 money update - fixed covers menu spawning too many covers
result
02  13:15 0,2 money update                              | Actually, I can't quite decide if the lines should double
01   - fixed covers menu spawning too many covers       | size like this. Maybe only if they're above a certain length?

Ex:
: 0,2 money update - 9-toolbar : broke class up into multiple functions
result
02  13:15 0,2 money update
01   - 9-toolbar : broke class up into multiple functions

Timecodes, prefixes:
_ muted     _--  _0,1
- owed           -0,1   I could add --- for auto-owed, but I'm not sure what for.
+ banked    +--  +0,1   Time above 8,0 in a day or 35,0 a week will auto '+' I think.

Commands:
/help                   Prints help.

/hln                    Hides line number bar. Or toggles.
/hide line numbers

/sp 01 02 05 08 11 ...  If the given line numbers are timelogs, and if they are banked, removes them from the bank.
/spend

/i 00 [normal ins]      Inserts a normal instruction at the line number given, pushing whatever's there down one.
/insert 00 [normal ins] This is probably subject to restrictions. I don't have a model in mind for how this should work.
|                       If I could... simply 'play' whatever instruction was given at that point in the list, as if the
|                       later lines didn't exist.
|                       The internal model would have to be less containerized for this to work, though. Hm.

/del 00                 Deletes whatever is denoted by the line number.

/edit                   Opens file in a texteditor for root-level editing.
|                       Don't make any mistakes, yo.
|                       On exiting the editor, or something similar, the script does a complete refresh.
|                         If I don't know how to do this, /edit will open the editor and exit the script
|                         so you'll have to restart it.
'''
