from typing import List, Type
from src.stub_libraries.stub_numpy import array
from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.model.permission import Permission
from .query.request import Request
from .storageException import StorageException
class Storage:
    def getObjects(self, clazz, request: Request) -> array():
        raise StorageException()
    def addObject(self, entity, request: Request) -> int:
        raise StorageException()
    def updateObject(self, entity, request: Request) -> None:
        raise StorageException()
    def removeObject(self, clazz, request: Request) -> None:
        raise StorageException()
    def getPermissions(self, ownerClass, ownerId: int, propertyClass, propertyId: int) -> array():
        raise StorageException()
    def addPermission(self, permission: Permission) -> None:
        raise StorageException()
    def removePermission(self, permission: Permission) -> None:
        raise StorageException()
    def getPermissions(self, ownerClass, propertyClass ) -> array():
        return self.getPermissions(ownerClass, 0, propertyClass, 0)
    def getObject(self, clazz, request: Request) -> Type:
        objects = self.getObjects(clazz, request)
        return objects[0] if objects else None
