from src.examples.program.traccar.api.baseObjectResource import BaseObjectResource
from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.group import Group
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.condition import Permission
from src.examples.program.traccar.storage.query.request import Request


class ExtendedObjectResource(BaseObjectResource):

    def __init__(self, baseClass):
        super().__init__(baseClass)

    def get(self, all, userId, groupId, deviceId):

        conditions = list()

        if all:
            if self.permissions_service.notAdmin(self.get_user_id()):
                conditions.append(Permission(User.__class__, self.get_user_id(), self.base_class))
        else:
            if userId == 0:
                conditions.append(Permission(User.__class__, self.get_user_id(), self.base_class))
            else:
                self.permissions_service.checkUser(self.get_user_id(), userId)
                conditions.append((Permission(User.__class__, userId, self.base_class)).exclude_groups())

        if groupId > 0:
            self.permissions_service.checkPermission(Group.__class__, self.get_user_id(), groupId)
            conditions.append((Permission(Group.__class__, groupId, self.base_class)).exclude_groups())
        if deviceId > 0:
            self.permissions_service.checkPermission(Device.__class__, self.get_user_id(), deviceId)
            conditions.append((Permission(Device.__class__, deviceId, self.base_class)).exclude_groups())

        return self.storage.getObjects(self.base_class, Request(Columns.All(), Condition.merge(conditions)))
