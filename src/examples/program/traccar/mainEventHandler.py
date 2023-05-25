from numpy import array

from src.examples.program.traccar.basePipelineFactory import BasePipelineFactory
from src.examples.program.traccar.baseProtocolDecoder import BaseProtocolDecoder
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.database.statisticManager import StatisticsManager
from src.examples.program.traccar.handler.ackowledgementHandler import AcknowledgementHandler
from src.examples.program.traccar.helper.dateUtil import DateUtil
from src.examples.program.traccar.helper.networkUtil import NetworkUtil
from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.connectionManager import ConnectionManager
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class MainEventHandler():

    _LOGGER = "LoggerFactory.getLogger(MainEventHandler.__class__)"



    def __init__(self, config, cacheManager, storage, connectionManager, statisticsManager):

        self._connectionlessProtocols = set()
        self._logAttributes = set()
        self._cacheManager = None
        self._storage = None
        self._connectionManager = None
        self._statisticsManager = None

        self._cacheManager = cacheManager
        self._storage = storage
        self._connectionManager = connectionManager
        self._statisticsManager = statisticsManager
        connectionlessProtocolList = config.getString(Keys.STATUS_IGNORE_OFFLINE)
        if connectionlessProtocolList is not None:
            self._connectionlessProtocols.addAll(array(connectionlessProtocolList.split("[, ]")))
        self._logAttributes.addAll(array(config.getString(Keys.LOGGER_ATTRIBUTES).split("[, ]")))

    def channelRead(self, ctx, msg):
        if isinstance(msg, Position):

            position = msg
            device = self._cacheManager.getObject(Device.__class__, position.getDeviceId())

            try:
                if PositionUtil.isLatest(self._cacheManager, position):
                    updatedDevice = Device()
                    updatedDevice.setId(position.getDeviceId())
                    updatedDevice.setPositionId(position.getId())
                    self._storage.updateObject(updatedDevice, Request(Columns.Include("positionId"), Condition.Equals("id", updatedDevice.getId())))

                    self._cacheManager.updatePosition(position)
                    self._connectionManager.updatePosition(True, position)
            except StorageException as error:
                MainEventHandler._LOGGER.warn("Failed to update device", error)

            builder = ""
            builder += ("[") + (NetworkUtil.session(ctx.channel())) + ("] ")
            builder += ("id: ") + (device.getUniqueId())
            for attribute in self._logAttributes:
                if attribute == "time":
                    builder += (", time: ") + (DateUtil.formatDate(position.getFixTime(), False))
                elif attribute == "position":
                    builder += (", lat: ") + ("{0:.5f}".format(position.getLatitude()))
                    builder += (", lon: ") + ("{0:.5f}".format(position.getLongitude()))
                elif attribute == "speed":
                    if position.getSpeed() > 0:
                        builder += (", speed: ") + ("{0:.1f}".format(position.getSpeed()))
                elif attribute == "course":
                    builder += (", course: ") + ("{0:.1f}".format(position.getCourse()))
                elif attribute == "accuracy":
                    if position.getAccuracy() > 0:
                        builder += (", accuracy: ") + ("{0:.1f}".format(position.getAccuracy()))
                elif attribute == "outdated":
                    if position.getOutdated():
                        builder += (", outdated")
                elif attribute == "invalid":
                    if not position.getValid():
                        builder += (", invalid")
                else:
                    value = position.getAttributes().get(attribute)
                    if value is not None:
                        builder += (", ") + (attribute) + (": ") + (value)
            MainEventHandler._LOGGER.info(str(builder))

            self._statisticsManager.registerMessageStored(position.getDeviceId(), position.getProtocol())

            ctx.writeAndFlush(AcknowledgementHandler.EventHandled(position))

    def channelActive(self, ctx):
        if not(isinstance(ctx.channel(), "DatagramChannel")):
            MainEventHandler._LOGGER.info("[{}] connected", NetworkUtil.session(ctx.channel()))

    def channelInactive(self, ctx):
        MainEventHandler._LOGGER.info("[{}] disconnected", NetworkUtil.session(ctx.channel()))
        self._closeChannel(ctx.channel())

        supportsOffline = BasePipelineFactory.getHandler(ctx.pipeline(), "HttpRequestDecoder.__class__") is None and not self._connectionlessProtocols.contains(ctx.pipeline().get(BaseProtocolDecoder.__class__).getProtocolName())
        self._connectionManager.deviceDisconnected(ctx.channel(), supportsOffline)

    def exceptionCaught(self, ctx, cause):
        while cause.getCause() is not None and cause.getCause() is not cause:
            cause = cause.getCause()
        MainEventHandler._LOGGER.info("[{}] error", NetworkUtil.session(ctx.channel()), cause)
        self._closeChannel(ctx.channel())

    def userEventTriggered(self, ctx, evt):
        if isinstance(evt, "IdleStateEvent"):
            MainEventHandler._LOGGER.info("[{}] timed out", NetworkUtil.session(ctx.channel()))
            self._closeChannel(ctx.channel())

    def _closeChannel(self, channel):
        if not(isinstance(channel, "DatagramChannel")):
            channel.close()
