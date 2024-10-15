from src.examples.program.traccar.api.security.serviceAccountUser import ServiceAccountUser
from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.model.calendar import Calendar
from src.examples.program.traccar.model.command import Command
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.groupedModel import GroupedModel
from src.examples.program.traccar.model.group import Group
from src.examples.program.traccar.model.managedUser import ManagedUser
from src.examples.program.traccar.model.notification import Notification
from src.examples.program.traccar.model.schedulable import Schedulable
from src.examples.program.traccar.model.server import Server
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.model.userRestriction import UserRestrictions
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class PermissionsService:



    def __init__(self, storage):

        self._storage = None
        self._server = None
        self._user = None

        self._storage = storage

    def getServer(self):
        if self._server is None:
            self._server = self._storage.getObject(Server.__class__, Request(Columns.All()))
        return self._server

    def getUser(self, userId):
        if self._user is None and userId > 0:
            if userId == ServiceAccountUser.ID:
                self._user = ServiceAccountUser()
            else:
                self._user = self._storage.getObject(User.__class__, Request(Columns.All(), Condition.Equals("id", userId)))
        return self._user

    def notAdmin(self, userId):
        return not self.getUser(userId).getAdministrator()

    def checkAdmin(self, userId):
        if not self.getUser(userId).getAdministrator():
            raise Exception("Administrator access required")

    def checkManager(self, userId):
        if (not self.getUser(userId).getAdministrator()) and self.getUser(userId).getUserLimit() == 0:
            raise Exception("Manager access required")

    class CheckRestrictionCallback:
        def denied(self, userRestrictions):
            pass

    def checkRestriction(self, userId, callback):
        if (not self.getUser(userId).getAdministrator()) and (callback.denied(self.getServer()) or callback.denied(self.getUser(userId))):
            raise Exception("Operation restricted")

    def checkEdit(self, userId, clazz, addition):
        if not self.getUser(userId).getAdministrator():
            denied = False
            if self.getServer().getReadonly() or self.getUser(userId).getReadonly():
                denied = True
            elif clazz is Device.__class__:
                denied = self.getServer().getDeviceReadonly() or self.getUser(userId).getDeviceReadonly() or addition and self.getUser(userId).getDeviceLimit() == 0
                if (not denied) and addition and self.getUser(userId).getDeviceLimit() > 0:
                    deviceCount = self._storage.getObjects(Device.__class__, Request(Columns.Include("id"), Condition.Permission(User.__class__, userId, Device.__class__))).size()
                    denied = deviceCount >= self.getUser(userId).getDeviceLimit()
            elif clazz is Command.__class__:
                denied = self.getServer().getLimitCommands() or self.getUser(userId).getLimitCommands()
            if denied:
                raise Exception("Write access denied")

    def checkEdit(self, userId, object, addition):
        if not self.getUser(userId).getAdministrator():
            self.checkEdit(userId, type(object), addition)
            if isinstance(object, GroupedModel):
                after = (object)
                if after.getGroupId() > 0:
                    before = None
                    if not addition:
                        before = self._storage.getObject(type(after), Request(Columns.Include("groupId"), Condition.Equals("id", after.getId())))
                    if before is None or before.getGroupId() != after.getGroupId():
                        self.checkPermission(Group.__class__, userId, after.getGroupId())
            if isinstance(object, Schedulable):
                after = (object)
                if after.getCalendarId() > 0:
                    before = None
                    if not addition:
                        before = self._storage.getObject(type(after), Request(Columns.Include("calendarId"), Condition.Equals("id", after.getId())))
                    if before is None or before.getCalendarId() != after.getCalendarId():
                        self.checkPermission(Calendar.__class__, userId, after.getCalendarId())
            if isinstance(object, Notification):
                after = (object)
                if after.getCommandId() > 0:
                    before = None
                    if not addition:
                        before = self._storage.getObject(type(after), Request(Columns.Include("commandId"), Condition.Equals("id", after.getId())))
                    if before is None or before.getCommandId() != after.getCommandId():
                        self.checkPermission(Command.__class__, userId, after.getCommandId())

    def checkUser(self, userId, managedUserId):
        if userId != managedUserId and not self.getUser(userId).getAdministrator():
            if (not self.getUser(userId).getManager()) or self._storage.getPermissions(User.__class__, userId, ManagedUser.__class__, managedUserId).isEmpty():
                raise Exception("User access denied")

    def checkUserUpdate(self, userId, before, after):
        if before.getAdministrator() != after.getAdministrator() or before.getDeviceLimit() != after.getDeviceLimit() or before.getUserLimit() != after.getUserLimit():
            self.checkAdmin(userId)
        user = self.getUser(userId)
        if user is not None and user.getExpirationTime() is not None and (before.getExpirationTime() != after.getExpirationTime()) and (after.getExpirationTime() is None or user.getExpirationTime().compareTo(after.getExpirationTime()) < 0):
            self.checkAdmin(userId)
        if before.getReadonly() != after.getReadonly() or before.getDeviceReadonly() != after.getDeviceReadonly() or before.getDisabled() != after.getDisabled() or before.getLimitCommands() != after.getLimitCommands() or before.getDisableReports() != after.getDisableReports() or before.getFixedEmail() != after.getFixedEmail():
            if userId == after.getId():
                self.checkAdmin(userId)
            elif after.getId() > 0:
                self.checkUser(userId, after.getId())
            else:
                self.checkManager(userId)
        if before.getFixedEmail() and before.getEmail() is not after.getEmail():
            self.checkAdmin(userId)

    def checkPermission(self, clazz, userId, objectId):
        if (not self.getUser(userId).getAdministrator()) and not(clazz is User.__class__ and userId == objectId):
            object = self._storage.getObject(clazz, Request(Columns.Include("id"), Condition.And(Condition.Equals("id", objectId), Condition.Permission(User.__class__, userId,ManagedUser.__class__ if clazz is User.__class__ else clazz))))
            if object is None:
                raise Exception(clazz.getSimpleName() + " access denied")
