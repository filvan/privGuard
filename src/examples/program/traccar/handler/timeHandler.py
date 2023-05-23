from numpy import array

from src.examples.program.traccar.baseProtocolDecoder import BaseProtocolDecoder
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.model.position import Position

class TimeHandler():


    def __init__(self, config):

        self._enabled = False
        self._useServerTime = False
        self._protocols = None

        self._enabled = config.hasKey(Keys.TIME_OVERRIDE)
        if self._enabled:
            self._useServerTime = config.getString(Keys.TIME_OVERRIDE).equalsIgnoreCase("serverTime")
        else:
            self._useServerTime = False
        protocolList = config.getString(Keys.TIME_PROTOCOLS)
        if protocolList is not None:
            self._protocols = array(protocolList.split("[, ]"))
        else:
            self._protocols = None

    def channelRead(self, ctx, msg):

        if self._enabled and isinstance(msg, Position) and (self._protocols is None or self._protocols.contains(ctx.pipeline().get(BaseProtocolDecoder.__class__).getProtocolName())):

            position = msg
            if self._useServerTime:
                position.setDeviceTime(position.getServerTime())
                position.setFixTime(position.getServerTime())
            else:
                position.setFixTime(position.getDeviceTime())

        ctx.fireChannelRead(msg)
