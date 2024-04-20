from app.logstream.molecules.DateHeaderLog import DateHeaderLog
from app.logstream.molecules.TimeLog import TimeLog
from app.logstream.molecules.NoteLog import NoteLog
from app.state.ViewState import ViewState
from app.enums.View import View

ViewState.set(View.Normal)
# ViewState.set(View.Compact)
# ViewState.set(View.Markdown)

stream = [
  [DateHeaderLog, '-1'],
  [TimeLog, '0,2 day begin'],
  [TimeLog, '0,1 ida idm connect'],
  [TimeLog, '0,2 ida idm connect'],
  [NoteLog, "Okay, okay. This issue doesn't have anything to do with me."],
  [NoteLog, "Share tokens are per user and per activity, so if you edit an author save, that just updates the data at the already known share code; you don't get a new one."],
  [NoteLog, "- In that case, Authors don't need the ability to re-fetch share links either. They still don't."],
  [NoteLog, "So yay, no work. I'm done working today. Ahh, Fridays..."],
  [TimeLog, "+0,3 logpy"],
  [NoteLog, "Lot of good work. I'm so excited."],

  [DateHeaderLog, ''],
  [TimeLog, '0,2 day begin'],
  [TimeLog, "1,2 ida idm connect -- write tests, talk jmaier, post tests, argue about what ''full test suite'' means..."],
  [NoteLog, "Not that anything is Frank's fault right now, I just wanna deal with any of this rn..."],
  [NoteLog, "I just wanna get IDA through..."],
  [TimeLog, "0,1 ida idm connect -- more messages"],
  [TimeLog, "0,1 ida idm connect"],
  [TimeLog, "_0,1 mental break"],
  [TimeLog, "_0,3 more mental break"],
  [NoteLog, "I'm still tired af, but I do think it helped."],
]

# Test saving and reloading
stream = [ [type, type.fromInput(s)] for type, s in stream ]
stream = [ [type, obj.save()] for type, obj in stream ]
stream = [ type.fromSave(s) for type, s in stream ]

# Test displaying to console
for log in stream:
  displayString = log.display()
  if displayString:
    print(displayString)
