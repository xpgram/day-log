"""
[ ] Manages a list of logs. Handles render-skipping of objects, like how a NoteLog might
    render only after a preceeding TimeLog.
    [ ] Can sort by date and render only those log items.
[ ] Responds to ViewState updates by rerendering each log object.
[ ] Input interprets commands and directs that input to the write class file.
"""

from app.system import Dispatcher, Utils
from app.constants import Events
from app.enums.View import View
from app.logstream.molecules.LogStreamMolecule import LogstreamMolecule
from app.logstream.molecules.DateHeaderLog import DateHeaderLog
from app.logstream.molecules.TimeLog import TimeLog
from app.logstream.molecules.NoteLog import NoteLog
import datetime


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
