import collections

from src.examples.program.traccar.handler.events.baseEventHandler import BaseEventHandler
from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class IgnitionEventHandler(BaseEventHandler):


    def __init__(self, cacheManager):

        self._cacheManager = None

        self._cacheManager = cacheManager

    def analyzePosition(self, position):
        device = self._cacheManager.getObject(Device.__class__, position.getDeviceId())
        if device is None or not PositionUtil.isLatest(self._cacheManager, position):
            return None

        result = None

        if position.hasAttribute(Position.KEY_IGNITION):
            ignition = position.getBoolean(Position.KEY_IGNITION)

            lastPosition = self._cacheManager.getPosition(position.getDeviceId())
            if lastPosition is not None and lastPosition.hasAttribute(Position.KEY_IGNITION):
                oldIgnition = lastPosition.getBoolean(Position.KEY_IGNITION)

                if ignition and not oldIgnition:
                    result = collections.singletonMap(Event(Event.TYPE_IGNITION_ON, position), position)
                elif (not ignition) and oldIgnition:
                    result = collections.singletonMap(Event(Event.TYPE_IGNITION_OFF, position), position)
        return result
