from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.geocoder.geocoder import Geocoder
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class GeocoderHandler():

    _LOGGER = "LoggerFactory.getLogger(GeocoderHandler.class)"


    def __init__(self, config, geocoder, cacheManager):

        self._geocoder = None
        self._cacheManager = None
        self._ignorePositions = False
        self._processInvalidPositions = False
        self._reuseDistance = 0

        self._geocoder = geocoder
        self._cacheManager = cacheManager
        self._ignorePositions = config.getBoolean(Keys.GEOCODER_IGNORE_POSITIONS)
        self._processInvalidPositions = config.getBoolean(Keys.GEOCODER_PROCESS_INVALID_POSITIONS)
        self._reuseDistance = config.getInteger(Keys.GEOCODER_REUSE_DISTANCE, 0)

    def channelRead(self, ctx, message):
        if isinstance(message, Position) and not self._ignorePositions:
            position = message
            if self._processInvalidPositions or position.getValid():
                if self._reuseDistance != 0:
                    lastPosition = self._cacheManager.getPosition(position.getDeviceId())
                    if lastPosition is not None and lastPosition.getAddress() is not None and position.getDouble(Position.KEY_DISTANCE) <= self._reuseDistance:
                        position.setAddress(lastPosition.getAddress())
                        ctx.fireChannelRead(position)
                        return

                self._geocoder.getAddress(position.getLatitude(), position.getLongitude(), ReverseGeocoderCallbackAnonymousInnerClass(self, ctx, position))
            else:
                ctx.fireChannelRead(position)
        else:
            ctx.fireChannelRead(message)

    class ReverseGeocoderCallbackAnonymousInnerClass(Geocoder.ReverseGeocoderCallback):


        def __init__(self, outerInstance, ctx, position):
            self._outerInstance = outerInstance
            self._ctx = ctx
            self._position = position

        def onSuccess(self, address):
            self._position.setAddress(address)
            self._ctx.fireChannelRead(self._position)

        def onFailure(self, e):
            GeocoderHandler._LOGGER.warn("Geocoding failed", e)
            self._ctx.fireChannelRead(self._position)
