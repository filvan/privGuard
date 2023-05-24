from src.examples.program.traccar.api.baseObjectResource import BaseObjectResource
from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.group import Group
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class ExtendedObjectResource(BaseObjectResource):

    def __init__(self, baseClass):
        super().__init__(baseClass)

    def get(self, all, userId, groupId, deviceId):

        conditions = list()

        if all:
            if self.permissionsService.notAdmin(self.getUserId()):
                conditions.append(Condition.Permission(User.__class__, self.getUserId(), self.baseClass))
        else:
            if userId == 0:
                conditions.append(Condition.Permission(User.__class__, self.getUserId(), self.baseClass))
            else:
                self.permissionsService.checkUser(self.getUserId(), userId)
                conditions.append((Condition.Permission(User.__class__, userId, self.baseClass)).excludeGroups())

        if groupId > 0:
            self.permissionsService.checkPermission(Group.__class__, self.getUserId(), groupId)
            conditions.append((Condition.Permission(Group.__class__, groupId, self.baseClass)).excludeGroups())
        if deviceId > 0:
            self.permissionsService.checkPermission(Device.__class__, self.getUserId(), deviceId)
            conditions.append((Condition.Permission(Device.__class__, deviceId, self.baseClass)).excludeGroups())

        return self.storage.getObjects(self.baseClass, Request(Columns.All(), Condition.merge(conditions)))
