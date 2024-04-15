from app.system import Dispatcher
from app.constants import Events
from app.enums.View import View

_viewState = View.Normal

class ViewState:
  @staticmethod
  def get() -> View:
    "Returns the current View state."
    return _viewState

  @staticmethod
  def set(view: View):
    "Sets the current View state and emits this as an event."
    global _viewState
    _viewState = view
    ViewState.announce()

  @staticmethod
  def announce():
    "Emits a global event carrying the current view state as data."
    Dispatcher.emit(Events.ViewStateUpdated, _viewState)
