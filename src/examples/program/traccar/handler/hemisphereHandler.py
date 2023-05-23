from src.examples.program.traccar.baseDataHandler import BaseDataHandler
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.model.position import Position

class HemisphereHandler(BaseDataHandler):
    def __init__(self, config):
        self._latitudeFactor = 0
        self._longitudeFactor = 0

        latitudeHemisphere = config.getString(Keys.LOCATION_LATITUDE_HEMISPHERE)
        if latitudeHemisphere is not None:
            if latitudeHemisphere.equalsIgnoreCase("N"):
                self._latitudeFactor = 1
            elif latitudeHemisphere.equalsIgnoreCase("S"):
                self._latitudeFactor = -1
        longitudeHemisphere = config.getString(Keys.LOCATION_LONGITUDE_HEMISPHERE)
        if longitudeHemisphere is not None:
            if longitudeHemisphere.equalsIgnoreCase("E"):
                self._longitudeFactor = 1
            elif longitudeHemisphere.equalsIgnoreCase("W"):
                self._longitudeFactor = -1

    def handlePosition(self, position):
        if self._latitudeFactor != 0:
            position.setLatitude(abs(position.getLatitude()) * self._latitudeFactor)
        if self._longitudeFactor != 0:
            position.setLongitude(abs(position.getLongitude()) * self._longitudeFactor)
        return position
