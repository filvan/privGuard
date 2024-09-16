from collections import OrderedDict

from numpy import array

from src.examples.program.traccar.config.config import Keys
from src.examples.program.traccar.model.permission import Permission
from .broadcastMessage import BroadcastMessage
from .broadcastService import BroadcastService

class MulticastBroadcastService(BroadcastService):

    _LOGGER = "LoggerFactory.getLogger(MulticastBroadcastService.class)"

    def __init__(self, config, objectMapper):

        self._objectMapper = None
        self._networkInterface = None
        self._port = 0
        self._group = None
        self._publisherSocket = None
        self._service = "Executors.newSingleThreadExecutor()"
        self._receiverBuffer = [0 for _ in range(4096)]
        self._listeners = array()
        self._receiver = "Runnable()"

        self._objectMapper = objectMapper
        self._port = config.getInteger(Keys.BROADCAST_PORT)
        interfaceName = config.getString(Keys.BROADCAST_INTERFACE)
        if interfaceName.find('.') >= 0 or interfaceName.find(':') >= 0:
            self._networkInterface = "NetworkInterface.getByInetAddress(InetAddress.getByName(interfaceName))"
        else:
            self._networkInterface = "NetworkInterface.getByName(interfaceName)"
        address = "InetAddress.getByName(config.getString(Keys.BROADCAST_ADDRESS))"
        self._group = "InetSocketAddress(address, self._port)"

    def singleInstance(self):
        return False

    def registerListener(self, listener):
        self._listeners.add(listener)

    def updateDevice(self, local, device):
        message = BroadcastMessage()
        message.setDevice(device)
        self._sendMessage(message)

    def updatePosition(self, local, position):
        message = BroadcastMessage()
        message.setPosition(position)
        self._sendMessage(message)

    def updateEvent(self, local, userId, event):
        message = BroadcastMessage()
        message.setUserId(userId)
        message.setEvent(event)
        self._sendMessage(message)

    def updateCommand(self, local, deviceId):
        message = BroadcastMessage()
        message.setCommandDeviceId(deviceId)
        self._sendMessage(message)

    def invalidateObject(self, local, clazz, id):
        message = BroadcastMessage()
        message.setChanges(OrderedDict(Permission.getKey(clazz), id))
        self._sendMessage(message)

    def invalidatePermission(self, local, clazz1, id1, clazz2, id2):
        message = BroadcastMessage()
        message.setChanges(OrderedDict(Permission.getKey(clazz1), id1, Permission.getKey(clazz2), id2))
        self._sendMessage(message)

    def _sendMessage(self, message):
        try:
            buffer = self._objectMapper.writeValueAsString(message).getBytes()
            packet = "DatagramPacket(buffer, len(buffer), self._group)"
            self._publisherSocket.send(packet)
        except Exception as e:
            MulticastBroadcastService._LOGGER.warn("Broadcast failed", e)

    def _handleMessage(self, message):
        if message.getDevice() is not None:
            self._listeners.forEach(lambda listener : listener.updateDevice(False, message.getDevice()))
        elif message.getPosition() is not None:
            self._listeners.forEach(lambda listener : listener.updatePosition(False, message.getPosition()))
        elif message.get_user_id() is not None and message.getEvent() is not None:
            self._listeners.forEach(lambda listener : listener.updateEvent(False, message.get_user_id(), message.getEvent()))
        elif message.getCommandDeviceId() is not None:
            self._listeners.forEach(lambda listener : listener.updateCommand(False, message.getCommandDeviceId()))
        elif message.getChanges() is not None:
            iterator = message.getChanges().entrySet().iterator()
            if iterator.hasNext():
                first = iterator.next()
                if iterator.hasNext():
                    second = iterator.next()
                    self._listeners.forEach(lambda listener : listener.invalidatePermission(False, Permission.getKeyClass(first.getKey()), first.getValue(), Permission.getKeyClass(second.getKey()), second.getValue()))
                else:
                    self._listeners.forEach(lambda listener : listener.invalidateObject(False, Permission.getKeyClass(first.getKey()), first.getValue()))

    def start(self):
        self._service.submit(self._receiver)

    def stop(self):
        self._service.shutdown()
