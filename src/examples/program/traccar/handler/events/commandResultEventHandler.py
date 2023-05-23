import collections

from src.examples.program.traccar.handler.events.baseEventHandler import BaseEventHandler
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position

class CommandResultEventHandler(BaseEventHandler):
    def __init__(self):
        pass

    def analyzePosition(self, position):
        commandResult = position.getAttributes().get(Position.KEY_RESULT)
        if commandResult is not None:
            event = Event(Event.TYPE_COMMAND_RESULT, position)
            event.set(Position.KEY_RESULT, str(commandResult))
            return collections.singletonMap(event, position)
        return None
