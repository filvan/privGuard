from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.database.statisticManager import StatisticsManager
from src.examples.program.traccar.geolocation.geolocationProvider import GeolocationProvider
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager


class GeolocationHandler():

    _LOGGER = "LoggerFactory.getLogger(GeolocationHandler.class)"


    def __init__(self, config, geolocationProvider, cacheManager, statisticsManager):

        self._geolocationProvider = None
        self._cacheManager = None
        self._statisticsManager = None
        self._processInvalidPositions = False
        self._reuse = False

        self._geolocationProvider = geolocationProvider
        self._cacheManager = cacheManager
        self._statisticsManager = statisticsManager
        self._processInvalidPositions = config.getBoolean(Keys.GEOLOCATION_PROCESS_INVALID_POSITIONS)
        self._reuse = config.getBoolean(Keys.GEOLOCATION_REUSE)

    def channelRead(self, ctx, message):
        if isinstance(message, Position):
            position = message
            if (position.getOutdated() or self._processInvalidPositions and (not position.getValid())) and position.getNetwork() is not None:
                if self._reuse:
                    lastPosition = self._cacheManager.getPosition(position.getDeviceId())
                    if lastPosition is not None and position.getNetwork() is lastPosition.getNetwork():
                        self._updatePosition(position, lastPosition.getLatitude(), lastPosition.getLongitude(), lastPosition.getAccuracy())
                        ctx.fireChannelRead(position)
                        return

                if self._statisticsManager is not None:
                    self._statisticsManager.registerGeolocationRequest()

                self._geolocationProvider.getLocation(position.getNetwork(), GeolocationProvider.LocationProviderCallback(self, ctx, position))
            else:
                ctx.fireChannelRead(position)
        else:
            ctx.fireChannelRead(message)

    class LocationProviderCallbackAnonymousInnerClass(GeolocationProvider.LocationProviderCallback):


        def __init__(self, outerInstance, ctx, position):
            self._outerInstance = outerInstance
            self._ctx = ctx
            self._position = position

        def onSuccess(self, latitude, longitude, accuracy):
            self._updatePosition(self._position, latitude, longitude, accuracy)
            self._ctx.fireChannelRead(self._position)

        def onFailure(self, e):
            GeolocationHandler._LOGGER.warn("Geolocation network error", e)
            self._ctx.fireChannelRead(self._position)

    def _updatePosition(self, position, latitude, longitude, accuracy):
        position.set(Position.KEY_APPROXIMATE, True)
        position.setValid(True)
        position.setFixTime(position.getDeviceTime())
        position.setLatitude(latitude)
        position.setLongitude(longitude)
        position.setAccuracy(accuracy)
        position.setAltitude(0)
        position.setSpeed(0)
        position.setCourse(0)
