from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position

class BroadcastInterface:

    def updateDevice(self, local, device):
        pass

    def updatePosition(self, local, position):
        pass

    def updateEvent(self, local, userId, event):
        pass

    def updateCommand(self, local, deviceId):
        pass

    def invalidateObject(self, local, clazz, id):
        pass

    def invalidatePermission(self, local, clazz1, id1, clazz2, id2):
        pass

