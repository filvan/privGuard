from src.examples.program.traccar.database.statisticManager import StatisticsManager
class Geocoder:

    class ReverseGeocoderCallback:

        def onSuccess(self, address):
            pass

        def onFailure(self, e):
            pass


    def getAddress(latitude, longitude, callback):
        pass

    def setStatisticsManager(statisticsManager):
        pass
