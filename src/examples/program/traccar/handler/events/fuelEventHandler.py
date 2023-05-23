from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.handler.events.baseEventHandler import BaseEventHandler
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.helper.model.attributeUtil import AttributeUtil
from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class FuelEventHandler(BaseEventHandler):


    def __init__(self, cacheManager):

        self._cacheManager = None

        self._cacheManager = cacheManager

    def analyzePosition(self, position):

        device = self._cacheManager.getObject(Device.__class__, position.getDeviceId())
        if device is None:
            return None
        if not PositionUtil.isLatest(self._cacheManager, position):
            return None

        if position.hasAttribute(Position.KEY_FUEL_LEVEL):
            lastPosition = self._cacheManager.getPosition(position.getDeviceId())
            if lastPosition is not None and lastPosition.hasAttribute(Position.KEY_FUEL_LEVEL):
                before = lastPosition.getDouble(Position.KEY_FUEL_LEVEL)
                after = position.getDouble(Position.KEY_FUEL_LEVEL)
                change = after - before

                if change > 0:
                    threshold = AttributeUtil.lookup(self._cacheManager, Keys.EVENT_FUEL_INCREASE_THRESHOLD, position.getDeviceId())
                    if threshold > 0 and change >= threshold:
                        return { Event(Event.TYPE_DEVICE_FUEL_INCREASE, position): position }
                elif change < 0:
                    threshold = AttributeUtil.lookup(self._cacheManager, Keys.EVENT_FUEL_DROP_THRESHOLD, position.getDeviceId())
                    if threshold > 0 and abs(change) >= threshold:
                        return { Event(Event.TYPE_DEVICE_FUEL_DROP, position): position }

        return None
