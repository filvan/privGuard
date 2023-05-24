from kafka.protocol.api import Response

from src.examples.program.traccar.api.baseResource import BaseResource
from src.examples.program.traccar.helper.logAction import LogAction
from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.model.group import Group
from src.examples.program.traccar.model.permission import Permission
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.session.connectionManager import ConnectionManager
from src.examples.program.traccar.session.cache.cacheManager import CacheManager
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class BaseObjectResource(BaseResource):




    def __init__(self, baseClass):

        self._cacheManager = None
        self._connectionManager = None
        self.baseClass = None

        self.baseClass = baseClass

    def getSingle(self, id):
        BaseResource.permissionsService.checkPermission(self.baseClass, BaseResource.getUserId(), id)
        entity = BaseResource.storage.getObject(self.baseClass, Request(Columns.All(), Condition.Equals("id", id)))
        if entity is not None:
            return Response.ok(entity).build()
        else:
            return Response.status(Response.Status.NOT_FOUND).build()

    def add(self, entity):
        BaseResource.permissionsService.checkEdit(BaseResource.getUserId(), entity, True)

        entity.setId(BaseResource.storage.addObject(entity, Request(Columns.Exclude("id"))))
        LogAction.create(BaseResource.getUserId(), entity)
        BaseResource.storage.addPermission(Permission(User.__class__, BaseResource.getUserId(), self.baseClass, entity.getId()))
        self._cacheManager.invalidatePermission(True, User.__class__, BaseResource.getUserId(), self.baseClass, entity.getId())
        self._connectionManager.invalidatePermission(True, User.__class__, BaseResource.getUserId(), self.baseClass, entity.getId())
        LogAction.link(BaseResource.getUserId(), User.__class__, BaseResource.getUserId(), self.baseClass, entity.getId())

        return Response.ok(entity).build()

    def update(self, entity):
        BaseResource.permissionsService.checkEdit(BaseResource.getUserId(), entity, False)
        BaseResource.permissionsService.checkPermission(self.baseClass,BaseResource.getUserId(), entity.getId())

        if isinstance(entity, User):
            before = BaseResource.storage.getObject(User.__class__, Request(Columns.All(), Condition.Equals("id", entity.getId())))
            BaseResource.permissionsService.checkUserUpdate(BaseResource.getUserId(), before, entity)
        elif isinstance(entity, Group):
            group = entity
            if group.getId() == group.getGroupId():
                raise Exception("Cycle in group hierarchy")

        BaseResource.storage.updateObject(entity, Request(Columns.Exclude("id"), Condition.Equals("id", entity.getId())))
        if isinstance(entity, User):
            user = entity
            if user.getHashedPassword() is not None:
                BaseResource.storage.updateObject(entity, Request(Columns.Include("hashedPassword", "salt"), Condition.Equals("id", entity.getId())))
        self._cacheManager.updateOrInvalidate(True, entity)
        LogAction.edit(BaseResource.getUserId(), entity)

        return Response.ok(entity).build()

    def remove(self, id):
        BaseResource.permissionsService.checkEdit(BaseResource.getUserId(), self.baseClass, False)
        BaseResource.permissionsService.checkPermission(self.baseClass, BaseResource.getUserId(), id)

        BaseResource.storage.removeObject(self.baseClass, Request(Condition.Equals("id", id)))
        self._cacheManager.invalidate(self.baseClass, id)

        LogAction.remove(BaseResource.getUserId(), self.baseClass, id)

        return Response.noContent().build()
