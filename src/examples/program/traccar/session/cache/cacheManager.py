from numpy import array

from src.examples.program.traccar.broadcast import broadcastService
from src.examples.program.traccar.broadcast.broadcastInterface import BroadcastInterface
from src.examples.program.traccar.broadcast.broadcastService import BroadcastService
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.model.attribute import Attribute
from src.examples.program.traccar.model.calendar import Calendar
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.driver import Driver
from src.examples.program.traccar.model.geofence import Geofence
from src.examples.program.traccar.model.group import Group
from src.examples.program.traccar.model.groupedModel import GroupedModel
from src.examples.program.traccar.model.maintenance import Maintenance
from src.examples.program.traccar.model.notification import Notification
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.schedulable import Schedulable
from src.examples.program.traccar.model.server import Server
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.session.cache.cacheKey import CacheKey
from src.examples.program.traccar.session.cache.cacheValue import CacheValue
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageName import StorageName
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request



class CacheManager(BroadcastInterface):

    _LOGGER = "LoggerFactory.getLogger(CacheManager.class)"
    _GROUP_DEPTH_LIMIT = 3
    _CLASSES = [Attribute.__class__, Driver.__class__, Geofence.__class__, Maintenance.__class__, Notification.__class__]





    def __init__(self, config, storage, broadcastService):

        self._config = None
        self._storage = None
        self._broadcastService = None
        self._lock = "ReentrantReadWriteLock()"
        self._deviceCache = {}
        self._deviceReferences = {}
        self._deviceLinks = {}
        self._devicePositions = {}
        self._server = None
        self._notificationUsers = {}

        self._config = config
        self._storage = storage
        self._broadcastService = broadcastService
        self._invalidateServer()
        self._invalidateUsers()
        broadcastService.registerListener(self)

    def getConfig(self):
        return self._config

    def getObject(self, clazz, id):
        try:
            self._lock.readLock().lock()
            cacheValue = self._deviceCache[CacheKey(clazz, id)]
            return cacheValue.getValue() if cacheValue is not None else None
        finally:
            self._lock.readLock().unlock()

    def getDeviceObjects(self, deviceId, clazz):
        try:
            self._lock.readLock().lock()
            links = self._deviceLinks[deviceId]
            if links is not None:
                pass
            else:
                CacheManager._LOGGER.warn("Device {} cache missing", deviceId)
                return []
        finally:
            self._lock.readLock().unlock()

    def getPosition(self, deviceId):
        try:
            self._lock.readLock().lock()
            return self._devicePositions[deviceId]
        finally:
            self._lock.readLock().unlock()

    def getServer(self):
        try:
            self._lock.readLock().lock()
            return self._server
        finally:
            self._lock.readLock().unlock()

    def getNotificationUsers(self, notificationId, deviceId):
        try:
            self._lock.readLock().lock()
            users = self._deviceLinks[deviceId][User.__class__].stream().collect([])
            return self._notificationUsers.getOrDefault(notificationId, array()).stream().filter(lambda user : users.contains(user.getId())).collect([])
        finally:
            self._lock.readLock().unlock()

    def findDriverByUniqueId(self, deviceId, driverUniqueId):
        return self.getDeviceObjects(deviceId, Driver.__class__).stream().filter(lambda driver : driver.getUniqueId() is driverUniqueId).findFirst().orElse(None)

    def addDevice(self, deviceId):
        try:
            self._lock.writeLock().lock()
            references = self._deviceReferences[deviceId]
            if references is not None:
                references += 1
            else:
                self._unsafeAddDevice(deviceId)
                references = 1
            self._deviceReferences[deviceId] = references
        finally:
            self._lock.writeLock().unlock()

    def removeDevice(self, deviceId):
        try:
            self._lock.writeLock().lock()
            references = self._deviceReferences[deviceId]
            if references is not None:
                references -= 1
                if references <= 0:
                    self._unsafeRemoveDevice(deviceId)
                    self._deviceReferences.pop(deviceId)
                else:
                    self._deviceReferences[deviceId] = references
        finally:
            self._lock.writeLock().unlock()

    def updatePosition(self, position):
        try:
            self._lock.writeLock().lock()
            if position.getDeviceId() in self._deviceLinks.keys():
                self._devicePositions[position.getDeviceId()] = position
        finally:
            self._lock.writeLock().unlock()

    def invalidateObject(self, local, clazz, id):
        try:
            object = self._storage.getObject(clazz, Request(Columns.All(), Condition.Equals("id", id)))
            if object is not None:
                self.updateOrInvalidate(local, object)
            else:
                self._invalidate(clazz, id)
        except Exception as e:
            raise Exception(e)



    def updateOrInvalidate(self, local, object):
        if local:
            broadcastService.invalidateObject(True, type(object), object.getId())

        if isinstance(object, Server):
            self._invalidateServer()
            return
        if isinstance(object, User):
            self._invalidateUsers()
            return

        invalidate = False
        before = self.getObject(type(object), object.getId())
        if before is None:
            return
        elif isinstance(object, GroupedModel):
            if (before).getGroupId() != (object).getGroupId():
                invalidate = True
        elif isinstance(object, Schedulable):
            if (before).getCalendarId() != (object).getCalendarId():
                invalidate = True
        if invalidate:
            self._invalidate(type(object), object.getId())
        else:
            try:
                self._lock.writeLock().lock()
                self._deviceCache.get(CacheKey(type(object), object.getId())).setValue(object)
            finally:
                self._lock.writeLock().unlock()




    def invalidate(self, clazz, id):
        self._invalidate(CacheKey(clazz, id))

    def invalidatePermission(self, local, clazz1, id1, clazz2, id2):
        if local:
            broadcastService.invalidatePermission(True, clazz1, id1, clazz2, id2)

        try:
            self._invalidate(CacheKey(clazz1, id1), CacheKey(clazz2, id2))
        except Exception as e:
            raise Exception(e)



    def _invalidateServer(self):
        self._server = self._storage.getObject(Server.__class__, Request(Columns.All()))


    def _invalidateUsers(self):
        self._notificationUsers.clear()
        users = {}
        self._storage.getObjects(User.__class__, Request(Columns.All())).forEach( lambda user: users.put(user.getId(), user))

    def _addObject(self, deviceId, object):
        self._deviceCache.computeIfAbsent(CacheKey(object), lambda k: CacheValue(object)).retain(deviceId)



    def _unsafeAddDevice(self, deviceId):
        links = {}

        device = self._storage.getObject(Device.__class__ , Request(Columns.All(), Condition.Equals("id", deviceId)))
        if device is not None:
            self._addObject(deviceId, device)

            groupDepth = 0
            groupId = device.getGroupId()
            while groupDepth < self._GROUP_DEPTH_LIMIT and groupId > 0:
                group = self._storage.getObject(Group.__class__ , Request(Columns.All(), Condition.Equals("id", groupId)))
                links.computeIfAbsent(Group.__class__, lambda k: array()).add(group.getId())
                self._addObject(deviceId, group)
                groupId = group.getGroupId()
                groupDepth += 1

            for clazz in self._CLASSES:
                objects = self._storage.getObjects(clazz, Request(Columns.All(), Condition.Permission(Device.__class__ , deviceId, clazz)))
                links[clazz] = objects.stream().map().collect([])
                for object in objects:
                    self._addObject(deviceId, object)
                if isinstance(object, Schedulable):
                    scheduled = object
                if scheduled.getCalendarId() > 0:
                    calendar = self._storage.getObject(Calendar.__class__ , Request(Columns.All(), Condition.Equals("id", scheduled.getCalendarId())))
                links.computeIfAbsent(Notification.__class__, lambda k: array()).add(calendar.getId())
                self._addObject(deviceId, calendar)

            users = self._storage.getObjects(User.__class__ , Request(Columns.All(), Condition.Permission(User.__class__ , Device.__class__, deviceId)))
            links[User.__class__ ] = users.stream().map().collect([])
            for user in users:
                self._addObject(deviceId, user)
                notifications = self._storage.getObjects(Notification.__class__ , Request(Columns.All(), Condition.Permission(User.__class__ , user.getId(), Notification.__class__ ))).stream().filter().collect([])
                for notification in notifications:
                    links.computeIfAbsent(Notification.__class__ , lambda k: array()).add(notification.getId())
                    self._addObject(deviceId, notification)
                    if notification.getCalendarId() > 0:
                        calendar = self._storage.getObject(Calendar.__class__, Request(Columns.All(), Condition.Equals("id", notification.getCalendarId())))
                        links.computeIfAbsent(Notification.__class__, lambda k: array()).add(calendar.getId())
                        self._addObject(deviceId, calendar)

            self._deviceLinks.put(deviceId, links)

            if device.getPositionId() > 0:
                self._devicePositions.put(deviceId, self._storage.getObject(Position.__class__ , Request(Columns.All(), Condition.Equals("id", device.getPositionId()))))


    def _unsafeRemoveDevice(self, deviceId):
        self.deviceCache.remove(CacheKey(Device.__class__ , deviceId))

        self._devicePositions.remove(deviceId)

    def _invalidate(self, *keys):
        try:
            self._lock.writeLock().lock()
            self._unsafeInvalidate(keys)
        finally:
            self._lock.writeLock().unlock()

    def _unsafeInvalidate(self, keys):
        invalidateServer = False
        invalidateUsers = False
        linkedDevices = array()
        for key in keys:
            if key.classIs(Server.__class__):
                invalidateServer = True

            else:
                if key.classIs(User.__class__ ) or key.classIs(Notification.__class__ ):
                        invalidateUsers = True

            for deviceId in linkedDevices:
                self._unsafeRemoveDevice(deviceId)
                self._unsafeAddDevice(deviceId)
            if invalidateServer:
                self._invalidateServer()
            if invalidateUsers:
                self._invalidateUsers()




