import collections

from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.session.connectionManager import ConnectionManager
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.storage import Storage


class AsyncSocket( ConnectionManager.UpdateListener):

    _LOGGER = "LoggerFactory.getLogger(AsyncSocket.class)"

    _KEY_DEVICES = "devices"
    _KEY_POSITIONS = "positions"
    _KEY_EVENTS = "events"


    def __init__(self, objectMapper, connectionManager, storage, userId):
        #instance fields found by Java to Python Converter:
        self._objectMapper = None
        self._connectionManager = None
        self._storage = None
        self._userId = 0

        self._objectMapper = objectMapper
        self._connectionManager = connectionManager
        self._storage = storage
        self._userId = userId

    def onWebSocketConnect(self, session):
        super().onWebSocketConnect(session)

        try:
            data = {}
            data[AsyncSocket._KEY_POSITIONS] = PositionUtil.getLatestPositions(self._storage, self._userId)
            self._sendData(data)
            self._connectionManager.addListener(self._userId, self)
        except StorageException as e:
            raise Exception(e)

    def onWebSocketClose(self, statusCode, reason):
        super().onWebSocketClose(statusCode, reason)

        self._connectionManager.removeListener(self._userId, self)

    def onKeepalive(self):
        self._sendData({})

    def onUpdateDevice(self, device):
        data = {}

        data[AsyncSocket._KEY_DEVICES] = collections.singletonList(device)

        self._sendData(data)

    def onUpdatePosition(self, position):
        data = {}
        data[AsyncSocket._KEY_POSITIONS] = collections.singletonList(position)
        self._sendData(data)

    def onUpdateEvent(self, event):
        data = {}
        data[AsyncSocket._KEY_EVENTS] = collections.singletonList(event)
        self._sendData(data)

    def _sendData(self, data):
        if self._isConnected():
            try:
                self.getRemote().sendString(self._objectMapper.writeValueAsString(data), None)
            except Exception as e:
                AsyncSocket._LOGGER.warn("Socket JSON formatting error", e)
