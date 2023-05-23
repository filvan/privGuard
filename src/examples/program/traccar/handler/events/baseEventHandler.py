from src.examples.program.traccar.baseDataHandler import BaseDataHandler
from src.examples.program.traccar.database.notificationManager import NotificationManager
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position

class BaseEventHandler(BaseDataHandler):

    def __init__(self):

        self._notificationManager = None



    def setNotificationManager(self, notificationManager):
        self._notificationManager = notificationManager

    def handlePosition(self, position):
        events = self.analyzePosition(position)
        if events is not None and events:
            self._notificationManager.updateEvents(events)
        return position

    def analyzePosition(self, position):
        pass
