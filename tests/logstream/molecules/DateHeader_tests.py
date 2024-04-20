
from app.logstream.atoms.Time import Time
from app.enums.View import View
from app.state.ViewState import ViewState
from app.system.Dispatcher import Dispatcher
from app.logstream.molecules.DateHeaderLog import DateHeaderLog
from datetime import datetime

ViewState.set(View.Normal)
ViewState.set(View.Compact)
# ViewState.set(View.Markdown)

inputs = [
  '',
  '1',
  '+1',
  '3',
  '-1',
  'a',
  '=1',
  'one',
  '-31',
  '+31',
  '365',
]

for input in inputs:
  try:
    obj = DateHeaderLog.fromInput(input)
    saveStr = obj.save()
    print(saveStr)
    print(obj.display())

    obj2 = DateHeaderLog.fromSave(saveStr)
    print(obj.display())
  except Exception as err:
    print(f'Failed: {err}')
  print()
