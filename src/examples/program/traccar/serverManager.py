from numpy import array

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.helper.classScanner import ClassScanner
from src.examples.program.traccar.lifecycleObject import LifecycleObject
from .baseProtocol import BaseProtocol
from .globalTimer import GlobalTimer


class ServerManager(LifecycleObject):

    _LOGGER = "LoggerFactory.getLogger(ServerManager.class)"


    def __init__(self, injector, config):

        self._connectorList = []
        self._protocolList = {}

        enabledProtocols = None
        if config.hasKey(Keys.PROTOCOLS_ENABLE):
            enabledProtocols = array((config.getString(Keys.PROTOCOLS_ENABLE).split("[, ]")))
        for protocolClass in ClassScanner.findSubclasses(BaseProtocol.__class__, "org.traccar.protocol"):
            protocolName = BaseProtocol.nameFromClass(protocolClass)
            if enabledProtocols is None or enabledProtocols.contains(protocolName):
                if config.hasKey(Keys.PROTOCOL_PORT.withPrefix(protocolName)):
                    protocol = injector.getInstance(protocolClass)
                    self._connectorList.extend(protocol.getConnectorList())
                    self._protocolList[protocol.getName()] = protocol

    def getProtocol(self, name):
        return self._protocolList[name]

    def start(self):
        for connector in self._connectorList:
            try:
                connector.start()
            except Exception as e:
                ServerManager._LOGGER.warn("Port disabled due to conflict", e)
            except Exception as e:
                ServerManager._LOGGER.warn("Connection failed", e)

    def stop(self):
        try:
            for connector in self._connectorList:
                connector.stop()
        finally:
            GlobalTimer.release()
