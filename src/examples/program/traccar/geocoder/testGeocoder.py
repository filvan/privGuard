from src.examples.program.traccar.geocoder.geocoder import Geocoder
from src.examples.program.traccar.database.statisticManager import StatisticsManager


class TestGeocoder(Geocoder):

    def setStatisticsManager(self, statisticsManager):
        pass

    def getAddress(self, latitude, longitude, callback):
        address = "Location {0:f}, {1:f}".format(latitude, longitude)
        if callback is not None:
            callback.onSuccess(address)
            return None
        return address
