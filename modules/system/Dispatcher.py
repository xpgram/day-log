from typing import Callable

# Types
type EventData = dict[str, any]
type EventCallback = Callable[[EventData], None]

_eventDictionary: dict[str, list[EventCallback]] = {}

def on(event: str, callback: EventCallback):
  """Registers a listener for an event. Will not register duplicate callbacks
  for the same event key."""

  if not _eventDictionary.get(event):
    _eventDictionary[event] = []
  if callback in _eventDictionary.get(event):
    return
  _eventDictionary[event].append(callback)

def off(event: str, callback: EventCallback):
  """Unregisters a listener for an event. If the event callback pair does not
  exist, does nothing."""

  callbacks = _eventDictionary.get(event)
  if not callbacks:
    return
  
  if callback in callbacks:
    callbacks.remove(callback)

def emit(event: str, data: EventData = {}):
  """Emits an event. For every listener to this event, calls their callback
  function."""

  callbacks = _eventDictionary.get(event)
  if not callbacks:
    return
  for callback in callbacks:
    callback(data)
