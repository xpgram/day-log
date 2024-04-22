from enum import Enum

TimecodeType = Enum('TimecodeType', [
    'Time',
    'Wildcard',
    'Banked',
    'Owed',
    'Muted',
    'Uncertain',
])
