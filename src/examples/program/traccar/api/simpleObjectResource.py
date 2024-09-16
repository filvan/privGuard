from src.examples.program.traccar.api.baseObjectResource import BaseObjectResource
from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Permission, Condition
from src.examples.program.traccar.storage.query.request import Request


class SimpleObjectResource(BaseObjectResource):

    def __init__(self, baseClass):
        super().__init__(baseClass)

    def get(self, all, userId):

        conditions = list()

        if all:
            if self.permissions_service.notAdmin(self.get_user_id()):
                conditions.append(Permission(User.__class__, self.get_user_id(), self.base_class))
        else:
            if userId == 0:
                userId = self.get_user_id()
            else:
                self.permissions_service.checkUser(self.get_user_id(), userId)
            conditions.append(Permission(User.__class__, userId, self.base_class))

        return self.storage.getObjects(self.base_class, Request(Columns.All(), Condition.merge(conditions)))
