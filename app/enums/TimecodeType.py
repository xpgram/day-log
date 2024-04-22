from enum import Enum

TimecodeType = Enum('TimecodeType', [
    'Time',
    'Banked',
    'Owed',
    'Muted',
    'Uncertain',
])
