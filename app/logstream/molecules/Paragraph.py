# I don't know if there's a use for this class, actually.
# Messages are actually displayed as separate lines.

# TODO LogLines that are too long should always wrap and indent.
# How do I model this?

"""
This atom is for this part.
|------------------------------------------------------------------------------|
12:31 +2,1 cras pulvinar - Mattis nunc sed blandit libero volutpat sed cras quis

Although, going by the examples I have below, maybe it's not.
- Messages can wrap themselves.
- Titles can as well, but they need to know their time and timecode to do it.
"""

def save():
  pass

def render():
  pass

"""
The idea with this one is to control line-wrapping during render, as well as any
other higher-level display concerns.

Off the top of my head:
- Text and text wrapping
  - Whether the text is indented or flat.
- LogStream ID (or 'line number')


Example text:

12:31 +2,1 cras pulvinar --
    Mattis nunc sed blandit libero volutpat sed cras quis
  vitae elementum curabitur vitae nunc sed velit dignissim sodales ut vel eros
  risus viverra adipiscing.
    At in tellus integer feugiat scelerisque varius nisl purus in mollis donec
  nunc sed id semper risus in.
    Egestas erat imperdiet sed euismod.
    Adipiscing elit ut aliquam purus sit amet luctus venenatis lectus magna
  fringilla urna porttitor rhoncus dolor purus non enim praesent elementum
  facilisis leo vel fringilla.
12:31 +2,1 cras pulvinar --
    Mattis nunc sed blandit libero volutpat sed cras quis vitae elementum
  curabitur vitae nunc sed velit dignissim sodales ut vel eros.
12:31 +2,1 A category title that is too long turpis egestas maecenas pharetra       Perhaps it should be truncated instead?
  convallis posuere morbi leo urna molestie at elementum. --
12:31 +2,1 cras pulvinar --
    Mattis nunc sed blandit libero volutpat sed cras quis.
    Vitae elementum curabitur vitae nunc sed.

12:31 +2,1 cras pulvinar --
 - Mattis nunc sed blandit libero volutpat sed cras quis
   vitae elementum curabitur vitae nunc sed velit dignissim sodales ut vel eros
   risus viverra adipiscing.
 - At in tellus integer feugiat scelerisque varius nisl purus in mollis donec
   nunc sed id semper risus in.
 - Egestas erat imperdiet sed euismod.
 - Adipiscing elit ut aliquam purus sit amet luctus venenatis lectus magna
   fringilla urna porttitor rhoncus dolor purus non enim praesent elementum
   facilisis leo vel fringilla.
12:31 +2,1 cras pulvinar --
 - Mattis nunc sed blandit libero volutpat sed cras quis vitae elementum
   curabitur vitae nunc sed velit dignissim sodales ut vel eros.
12:31 +2,1 A category title that is too long turpis egestas maecenas pharetra       Perhaps it should be truncated instead?
  convallis posuere morbi leo urna molestie at elementum. --
12:31 +2,1 cras pulvinar --
 - Mattis nunc sed blandit libero volutpat sed cras quis.
 - Vitae elementum curabitur vitae nunc sed.
"""
