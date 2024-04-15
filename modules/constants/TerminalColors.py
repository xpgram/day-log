
_Chars = {
  'EscapeChar': '\033',
}

TextStyle = {
  'Bold'       : '[1m',
  'Thin'       : '[2m',
  'Italic'     : '[3m',
  'Underline'  : '[4m',
  'SlowBlink'  : '[5m',
  'FastBlink'  : '[6m',
  'Strikethrough': '[9m',

  'FontDefault': '[10m',
  'Font2'      : '[11m',
  'Font3'      : '[12m',
  'Font4'      : '[13m',
  'Font5'      : '[14m',
  'Font6'      : '[15m',
  'Font7'      : '[16m',
  'Font8'      : '[17m',
  'Font9'      : '[18m',
  'Font10'     : '[19m',
}

# TODO Verify color names
TextColor = {
  'NoColor'    : '[0m',
  'Reset'      : '[39m',
  'Black'      : '[30m',
  'Red'        : '[31m',
  'Green'      : '[32m',
  'Orange'     : '[33m',
  'Blue'       : '[34m',
  'Magenta'    : '[35m',
  'Cyan'       : '[36m',
  'Gray'       : '[37m',
  'DarkGray'   : '[90m',
  'LightRed'   : '[91m',
  'LightGreen' : '[92m',
  'Yellow'     : '[93m',
  'LightBlue'  : '[94m',
  'Pink'       : '[95m',
  'LightCyan'  : '[96m',
  'White'      : '[97m',
}

TextBgColor = {
  'NoColor'    : '[0m',   # TODO This is the reset code for both text and back. Shouldn't these be consolidated?
  'Reset'      : '[49m',
  'Black'      : '[40m',
  'Red'        : '[41m',
  'Green'      : '[42m',
  'Orange'     : '[43m',
  'Blue'       : '[44m',
  'Magenta'    : '[45m',
  'Cyan'       : '[46m',
  'Gray'       : '[47m',
  'DarkGray'   : '[100m',
  'LightRed'   : '[101m',
  'LightGreen' : '[102m',
  'Yellow'     : '[103m',
  'LightBlue'  : '[104m',
  'Pink'       : '[105m',
  'LightCyan'  : '[106m',
  'White'      : '[107m',
}

# Process dictionaries to include escape chars before their codes.
for colorDict in [TextStyle, TextColor, TextBgColor]:
    for key in colorDict:
        colorDict[key] = _Chars['EscapeChar'] + colorDict[key]


def wrapText(styles: str | list[str], text: str):
    """Given a list of TerminalColor styles and a string, returns a new string with the
    content of the given string wrapped in style codes that enable and disable the given
    styles."""
    if type(styles) != list:
        styles = [styles]
    styleCodes = ''.join(styles)
    return f'{styleCodes}{text}{TextColor['NoColor']}'
