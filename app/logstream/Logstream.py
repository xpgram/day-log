"""
[ ] Manages a list of logs. Handles render-skipping of objects, like how a NoteLog might
    render only after a preceeding TimeLog.
    [ ] Can sort by date and render only those log items.
[ ] Responds to ViewState updates by rerendering each log object.
[ ] Input interprets commands and directs that input to the write class file.
"""

from app.system.Dispatcher import Dispatcher
from app.system.Utils import Utils
from app.constants import Events
from app.enums.View import View
from app.logstream.molecules.LogstreamMolecule import LogstreamMolecule
from app.logstream.molecules.DateHeaderLog import DateHeaderLog
from app.logstream.molecules.TimeLog import TimeLog
from app.logstream.molecules.NoteLog import NoteLog
import datetime


# TODO Loading from save
# One of the initial goals was to have a readable save file. At the very least a space efficient one.
# Some of this might be unrealistic, but there isn't really a reason a format like this:
#   Thu Feb 13, 2024
#   08:31 0,2 day begin
#   08:45 0,1 slack talk - cards don't save anymore, apparently
#    - Not my fault, at least.
#   09:28 0,3 ida idm conn - working out remaining todos.
# Couldn't be understood to be Feb 13 at different postage times.
# When loaded, the Logstream keeps in mind the most recently read date and passes it along
# to any other logs it creates. This way, they can still render themselves by date, but
# their data doesn't have to clutter the f- out of the save file.
# TODO The only question is what to do if the date header is missing for some reason...


class Logstream:
  stream: list[LogstreamMolecule] = []

  def __init__(self):
    Dispatcher.on(Events.ViewStateUpdated, self.updateRenderCache)

  def save(self):
    pass

    # TODO
    # How should this work?
    # Do we save the entire list? I think that's what the function would do.
    # But I want logstream objects to save in realtime. Manage the save file per submission.

  def updateRenderCache(self, view: View):
    for log in self.stream:
      log.cacheRender(view)

  def display(self, start: datetime = None, end: datetime = None):
    # TODO start/end is for narrowing the print range
    #   Or should the range be defined by a new state?
    #   I do kinda like that idea.
    #   Waait...
    #   Logs could listen for DateRangeState updates and choose themselves whether they
    #   display. Hm... interesting.
    #   [ ] Do Logs need to know who their parent DateHeader is? Like a carry-forward. Or can they just use their own datetime creation stamp?

    lines = [ log.display() for log in self.stream ]
    printable = '\n'.join(lines)
    print(printable)

    # TODO
    # Ranges, though?
    # Or partial updates?

  def input(self, data):
    command, data = Utils.getToken(data)

    switch = {
      '\d': DateHeaderLog,
    }
    method = switch.get(command, NoteLog)
    object = method.fromInput(data)

    # This has a lot of responsibility. I wonder if it should be broken up.
    # Problems during .fromInput() need to be handled simply.
    #   Display a message to... the marquee? I need a marquee.
    #   And then, I guess, just don't add the new object to self.stream.
    # [ ] Goal 1: Given a hardcoded list, render the list.
    pass
