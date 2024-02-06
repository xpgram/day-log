
dataFilePath = "./logpy_data"

helpText = '''
Not written.
'''.strip()

class viewport:
  width = 100,
  height = 50,   # TODO Can this be informed at runtime by actual height?

class charCodes:
  'A dictionary of special text-mode char sequences recognized by the terminal.'

  EscapeChar = '\033'

  class textStyle:
    Bold = '[1m'
    Thin = '[2m'
    Italic = '[3m'
    Underline = '[4m'
    SlowBlink = '[5m'
    FastBlink = '[6m'
    Strikethrough = '[9m'
    FontDefault = '[10m'
    Font2 = '[11m'
    Font3 = '[12m'
    Font4 = '[13m'
    Font5 = '[14m'
    Font6 = '[15m'
    Font7 = '[16m'
    Font8 = '[17m'
    Font9 = '[18m'
    Font10 = '[19m'

  class textColor:
    NoColor = '[0m'
    Reset = '[39m'
    Black = '[30m'
    Red = '[31m'
    Green = '[32m'
    Orange = '[33m'
    Blue = '[34m'
    Magenta = '[35m'
    Cyan = '[36m'
    Gray = '[37m'
    DarkGray = '[90m'
    LightRed = '[91m'
    LightGreen = '[92m'
    Yellow = '[93m'
    LightBlue = '[94m'
    Pink = '[95m'
    LightCyan = '[96m'
    White = '[97m'

  class textBgColor:
    NoColor = '[0m'   # TODO This is the reset code for both text and back. Shouldn't these be consolidated?
    Reset = '[49m'
    Black = '[40m'
    Red = '[41m'
    Green = '[42m'
    Orange = '[43m'
    Blue = '[44m'
    Magenta = '[45m'
    Cyan = '[46m'
    Gray = '[47m'
    DarkGray = '[100m'
    LightRed = '[101m'
    LightGreen = '[102m'
    Yellow = '[103m'
    LightBlue = '[104m'
    Pink = '[105m'
    LightCyan = '[106m'
    White = '[107m'

# Process each char-code dictionary to include the escape char before their unique codes.
for charCodeDict in [charCodes.textStyle, charCodes.textColor, charCodes.textBgColor]:
  for key in charCodeDict:
    charCodeDict[key] = f'{charCodes.EscapeChar}{charCodeDict[key]}'
