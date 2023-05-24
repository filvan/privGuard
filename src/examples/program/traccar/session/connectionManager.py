import collections

from numpy import array

from src.examples.program.traccar.broadcast import broadcastService
from src.examples.program.traccar.protocol import Protocol
from src.examples.program.traccar.broadcast.broadcastInterface import BroadcastInterface
from src.examples.program.traccar.broadcast.broadcastService import BroadcastService
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.database.deviceLookupService import DeviceLookupService
from src.examples.program.traccar.database.notificationManager import NotificationManager
from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.session.cache.cacheManager import CacheManager
from src.examples.program.traccar.session.deviceSession import DeviceSession
from src.examples.program.traccar.session.enpoint import Endpoint
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class ConnectionManager(BroadcastInterface):

    _LOGGER = "LoggerFactory.getLogger(ConnectionManager.__class__)"

    def __init__(self, config, cacheManager, storage, notificationManager, timer, broadcastService, deviceLookupService):

        self._deviceTimeout = 0
        self._sessionsByDeviceId = {}
        self._sessionsByEndpoint = {}
        self._config = None
        self._cacheManager = None
        self._storage = None
        self._notificationManager = None
        self._timer = None
        self._broadcastService = None
        self._deviceLookupService = None
        self._listeners = {}
        self._userDevices = {}
        self._deviceUsers = {}
        self._timeouts = {}

        self._config = config
        self._cacheManager = cacheManager
        self._storage = storage
        self._notificationManager = notificationManager
        self._timer = timer
        self._broadcastService = broadcastService
        self._deviceLookupService = deviceLookupService
        self._deviceTimeout = config.getLong(Keys.STATUS_TIMEOUT)
        broadcastService.registerListener(self)

    def getDeviceSession(self, deviceId):
        return self._sessionsByDeviceId[deviceId]

    def getDeviceSession(self, protocol, channel, remoteAddress, *uniqueIds):

        endpoint = (channel, remoteAddress)
        endpointSessions = self._sessionsByEndpoint.getOrDefault(endpoint, {})

        uniqueIds = array(uniqueIds).filter().toArray(str())
        if len(uniqueIds) > 0:
            for uniqueId in uniqueIds:
                deviceSession = endpointSessions[uniqueId]
                if deviceSession is not None:
                    return deviceSession
        else:
            return endpointSessions.values().stream().findAny().orElse(None)

        device = self._deviceLookupService.lookup(uniqueIds)

        if device is None and self._config.getBoolean(Keys.DATABASE_REGISTER_UNKNOWN):
            if uniqueIds[0].matches(self._config.getString(Keys.DATABASE_REGISTER_UNKNOWN_REGEX)):
                device = self._addUnknownDevice(uniqueIds[0])

        if device is not None:
            device.checkDisabled()

            oldSession = self._sessionsByDeviceId.pop(device.getId())
            if oldSession is not None:
                oldEndpoint = Endpoint(oldSession.getChannel(), oldSession.getRemoteAddress())
                oldEndpointSessions = self._sessionsByEndpoint[oldEndpoint]
                if oldEndpointSessions is not None and len(oldEndpointSessions) > 1:
                    oldEndpointSessions.pop(device.getUniqueId())
                else:
                    self._sessionsByEndpoint.pop(oldEndpoint)

            deviceSession = DeviceSession(device.getId(), device.getUniqueId(), protocol, channel, remoteAddress)
            endpointSessions[device.getUniqueId()] = deviceSession
            self._sessionsByEndpoint[endpoint] = endpointSessions
            self._sessionsByDeviceId[device.getId()] = deviceSession

            if oldSession is None:
                self._cacheManager.addDevice(device.getId())

            return deviceSession
        else:
            ConnectionManager._LOGGER.warn("Unknown device - " + str.join(" ", uniqueIds) + " (" + (remoteAddress).getHostString() + ")")
            return None

    def _addUnknownDevice(self, uniqueId):
        device = Device()
        device.setName(uniqueId)
        device.setUniqueId(uniqueId)
        device.setCategory(self._config.getString(Keys.DATABASE_REGISTER_UNKNOWN_DEFAULT_CATEGORY))

        defaultGroupId = self._config.getLong(Keys.DATABASE_REGISTER_UNKNOWN_DEFAULT_GROUP_ID)
        if defaultGroupId != 0:
            device.setGroupId(defaultGroupId)

        try:
            device.setId(self._storage.addObject(device, Request(Columns.Exclude("id"))))
            ConnectionManager._LOGGER.info("Automatically registered " + uniqueId)
            return device
        except StorageException as e:
            ConnectionManager._LOGGER.warn("Automatic registration failed", e)
            return None

    def deviceDisconnected(self, channel, supportsOffline):
        endpoint = Endpoint(channel, channel.remoteAddress())
        endpointSessions = self._sessionsByEndpoint.pop(endpoint)
        if endpointSessions is not None:
            for deviceSession in endpointSessions.values():
                if supportsOffline:
                    self.updateDevice(deviceSession.getDeviceId(), Device.STATUS_OFFLINE, None)
                self._sessionsByDeviceId.pop(deviceSession.getDeviceId())
                self._cacheManager.removeDevice(deviceSession.getDeviceId())

    def deviceUnknown(self, deviceId):
        self.updateDevice(deviceId, Device.STATUS_UNKNOWN, None)
        self._removeDeviceSession(deviceId)

    def _removeDeviceSession(self, deviceId):
        deviceSession = self._sessionsByDeviceId.pop(deviceId)
        if deviceSession is not None:
            self._cacheManager.removeDevice(deviceId)
            endpoint = Endpoint(deviceSession.getChannel(), deviceSession.getRemoteAddress())








    def updateDevice(self, local, device):
        if local:
            self._broadcastService.updateDevice(True, device)
        elif Device.STATUS_ONLINE is device.getStatus():
            self._timeouts.remove(device.getId())
            self._removeDeviceSession(device.getId())
        for userId in self._deviceUsers.getOrDefault(device.getId(), collections.emptySet()):
            if self._listeners.containsKey(userId):
                for listener in self._listeners.get(userId):
                    listener.onUpdateDevice(device)



    def updatePosition(self, local, position):
        if local:
            broadcastService.updatePosition(True, position)
        for userId in self._deviceUsers.getOrDefault(position.getDeviceId(), collections.emptySet()):
            if self._listeners.containsKey(userId):
                for listener in self._listeners.get(userId):
                    listener.onUpdatePosition(position)



    def updateEvent(self, local, userId, event):
        if local:
            broadcastService.updateEvent(True, userId, event)
        if self._listeners.containsKey(userId):
            for listener in self._listeners.get(userId):
                listener.onUpdateEvent(event)



    def invalidatePermission(self, local, clazz1, id1, clazz2, id2):
        if clazz1 is User.__class__ and clazz2 is Device.__class__:
            if self._listeners.containsKey(id1):
                self._userDevices.get(id1).add(id2)
                self._deviceUsers.put(id2, [])

    class UpdateListener:
        def onKeepalive(self):
            pass

        def onUpdateDevice(self, device):
            pass

        def onUpdatePosition(self, position):
            pass

        def onUpdateEvent(self, event):
            pass




    def addListener(self, userId, listener):
        set = self._listeners.get(userId)
        if set is None:
            set = []
            self._listeners.put(userId, set)

            devices = self._storage.getObjects(Device.__class__, Request(Columns.Include("id"), Condition.Permission(User.__class__ , userId, Device.__class__ )))
        self._userDevices.put(userId, devices.stream().map(BaseModel.getId()).collect(collections.toSet()))
        devices.forEach(lambda device: self._deviceUsers.computeIfAbsent(device.getId(), lambda id: []).add(userId))
        set.add(listener)



    def removeListener(self, userId, listener):
        set = self._listeners.get(userId)
        set.remove(listener)
        if set.isEmpty():
            self._listeners.remove(userId)


