from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.speedlimit.speedLimitProvider import SpeedLimitProvider

class SpeedLimitHandler():

    _LOGGER = "LoggerFactory.getLogger(SpeedLimitHandler.class)"


    def __init__(self, speedLimitProvider):

        self._speedLimitProvider = None

        self._speedLimitProvider = speedLimitProvider

    def channelRead(self, ctx, message):
        if isinstance(message, Position):
            position = message
            self._speedLimitProvider.getSpeedLimit(position.getLatitude(), position.getLongitude(), SpeedLimitProviderCallbackAnonymousInnerClass(self, ctx, position))
        else:
            ctx.fireChannelRead(message)

    class SpeedLimitProviderCallbackAnonymousInnerClass(SpeedLimitProvider.SpeedLimitProviderCallback):


        def __init__(self, outerInstance, ctx, position):
            self._outerInstance = outerInstance
            self._ctx = ctx
            self._position = position

        def onSuccess(self, speedLimit):
            self._position.set(Position.KEY_SPEED_LIMIT, speedLimit)
            self._ctx.fireChannelRead(self._position)

        def onFailure(self, e):
            SpeedLimitHandler._LOGGER.warn("Speed limit provider failed", e)
            self._ctx.fireChannelRead(self._position)
