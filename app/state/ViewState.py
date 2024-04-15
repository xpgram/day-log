from system import Dispatcher
from constants import Events
from enums.View import View

_viewState = View.Normal

def get() -> View:
  "Returns the current View state."
  return _viewState

def set(view: View):
  "Sets the current View state and emits this as an event."
  global _viewState
  _viewState = view
  announce()

def announce():
  "Emits a global event carrying the current view state as data."
  Dispatcher.emit(Events.ViewStateUpdated, _viewState)
