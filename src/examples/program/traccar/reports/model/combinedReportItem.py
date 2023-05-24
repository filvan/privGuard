from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position

class CombinedReportItem:

    def __init__(self):
        self._deviceId = 0
        self._route = None
        self._events = None
        self._positions = None



    def getDeviceId(self):
        return self._deviceId

    def setDeviceId(self, deviceId):
        self._deviceId = deviceId


    def getRoute(self):
        return self._route

    def setRoute(self, route):
        self._route = route


    def getEvents(self):
        return self._events

    def setEvents(self, events):
        self._events = events


    def getPositions(self):
        return self._positions

    def setPositions(self, positions):
        self._positions = positions
