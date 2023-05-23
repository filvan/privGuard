from src.examples.program.traccar.handler.events.baseEventHandler import BaseEventHandler
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position

class MediaEventHandler(BaseEventHandler):

    def __init__(self):
        pass

    def analyzePosition(self, position):
        #        return Stream.of(Position.KEY_IMAGE, Position.KEY_VIDEO, Position.KEY_AUDIO).filter(position::hasAttribute).map(type ->
        #        {
        #                    Event event = new Event(Event.TYPE_MEDIA, position)
        #                    event.set("media", type)
        #                    event.set("file", position.getString(type))
        #                    return event
        #                }
        #                ).collect(Collectors.toMap(event -> event, event -> position))
        pass
