from src.examples.program.traccar.model.network import Network
class GeolocationProvider:

    class LocationProviderCallback:

        def onSuccess(self, latitude, longitude, accuracy):
            pass

        def onFailure(self, e):
            pass


    def getLocation(network:Network, callback):
        pass
