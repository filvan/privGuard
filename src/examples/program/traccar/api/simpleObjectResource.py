from src.examples.program.traccar.api.baseObjectResource import BaseObjectResource
from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class SimpleObjectResource(BaseObjectResource):

    def __init__(self, baseClass):
        super().__init__(baseClass)

    def get(self, all, userId):

        conditions = list()

        if all:
            if self.permissionsService.notAdmin(self.getUserId()):
                conditions.add(Condition.Permission(User.__class__, self.getUserId(), self.baseClass))
        else:
            if userId == 0:
                userId = self.getUserId()
            else:
                self.permissionsService.checkUser(self.getUserId(), userId)
                conditions.add(Condition.Permission(User.__class__, userId, self.baseClass))

        return self.storage.getObjects(self.baseClass, Request(Columns.All(), Condition.merge(conditions)))
