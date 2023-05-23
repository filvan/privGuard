import decimal

from src.examples.program.traccar.baseDataHandler import BaseDataHandler
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.helper.distanceCalculator import DistanceCalculator
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class DistanceHandler(BaseDataHandler):



    def __init__(self, config, cacheManager):

        self._cacheManager = None
        self._filter = False
        self._coordinatesMinError = 0
        self._coordinatesMaxError = 0

        self._cacheManager = cacheManager
        self._filter = config.getBoolean(Keys.COORDINATES_FILTER)
        self._coordinatesMinError = config.getInteger(Keys.COORDINATES_MIN_ERROR)
        self._coordinatesMaxError = config.getInteger(Keys.COORDINATES_MAX_ERROR)

    def handlePosition(self, position):

        distance = 0.0
        if position.hasAttribute(Position.KEY_DISTANCE):
            distance = position.getDouble(Position.KEY_DISTANCE)
        totalDistance = 0.0

        last = self._cacheManager.getPosition(position.getDeviceId())
        if last is not None:
            totalDistance = last.getDouble(Position.KEY_TOTAL_DISTANCE)
            if not position.hasAttribute(Position.KEY_DISTANCE):
                distance = DistanceCalculator.distance(position.getLatitude(), position.getLongitude(), last.getLatitude(), last.getLongitude())
                distance = decimal.valueOf(distance).setScale(2, round().HALF_EVEN).doubleValue()
            if self._filter and last.getLatitude() != 0 and last.getLongitude() != 0:
                satisfiesMin = self._coordinatesMinError == 0 or distance > self._coordinatesMinError
                satisfiesMax = self._coordinatesMaxError == 0 or distance < self._coordinatesMaxError
                if (not satisfiesMin) or not satisfiesMax:
                    position.setValid(last.getValid())
                    position.setLatitude(last.getLatitude())
                    position.setLongitude(last.getLongitude())
                    distance = 0
        position.set(Position.KEY_DISTANCE, distance)
        totalDistance = decimal.valueOf(totalDistance + distance).setScale(2, round().HALF_EVEN).doubleValue()
        position.set(Position.KEY_TOTAL_DISTANCE, totalDistance)

        return position
