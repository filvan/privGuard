from kafka.protocol.api import Response

from src.examples.program.traccar.api.baseObjectResource import BaseObjectResource
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.helper.logAction import LogAction
from src.examples.program.traccar.helper.model.userUtil import UserUtil
from src.examples.program.traccar.model.managedUser import ManagedUser
from src.examples.program.traccar.model.permission import Permission
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class UserResource(BaseObjectResource):


    def __init__(self):

        self._config = None

        super().__init__(User.__class__)

    def get(self, userId):
        if userId > 0:
            self.permissions_service.checkUser(self.get_user_id(), userId)
            return self.storage.getObjects(self.base_class, Request(Columns.All(), (Condition.Permission(User.__class__, userId, ManagedUser.__class__)).excludeGroups()))
        elif self.permissions_service.notAdmin(self.get_user_id()):
            return self.storage.getObjects(self.base_class, Request(Columns.All(), (Condition.Permission(User.__class__, self.get_user_id(), ManagedUser.__class__)).excludeGroups()))
        else:
            return self.storage.getObjects(self.base_class, Request(Columns.All()))

    def add(self, entity):
        currentUser = self.permissions_service.getUser(self.get_user_id()) if self.get_user_id() > 0 else None
        if currentUser is None or not currentUser.getAdministrator():
            self.permissions_service.checkUserUpdate(self.get_user_id(), User(), entity)
            if currentUser is not None and currentUser.getUserLimit() != 0:
                userLimit = currentUser.getUserLimit()
                if userLimit > 0:
                    userCount = self.storage.getObjects(self.base_class, Request(Columns.All(), (Condition.Permission(User.__class__, self.get_user_id(), ManagedUser.__class__)).excludeGroups())).size()
                    if userCount >= userLimit:
                        raise Exception("Manager user limit reached")
            else:
                if not self.permissions_service.getServer().getRegistration():
                    raise Exception("Registration disabled")
                UserUtil.setUserDefaults(entity, self._config)

        if UserUtil.isEmpty(self.storage):
            entity.setAdministrator(True)

        entity.setId(self.storage.addObject(entity, Request(Columns.Exclude("id"))))
        self.storage.updateObject(entity, Request(Columns.Include("hashedPassword", "salt"), Condition.Equals("id", entity.getId())))

        LogAction.create(self.get_user_id(), entity)

        if currentUser is not None and currentUser.getUserLimit() != 0:
            self.storage.addPermission(Permission(User.__class__, self.get_user_id(), ManagedUser.__class__, entity.getId()))
            LogAction.link(self.get_user_id(), User.__class__, self.get_user_id(), ManagedUser.__class__, entity.getId())
        return Response.ok(entity).build()
