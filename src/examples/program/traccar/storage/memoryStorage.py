from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.model.pair import Pair
from src.examples.program.traccar.model.permission import Permission
from src.examples.program.traccar.model.server import Server
from .query.condition import Condition
from .query.request import Request
from collections import OrderedDict
from atomiclong import AtomicLong
from array import array
class MemoryStorage(Storage):

    def __init__(self):
        self._objects = {}
        self._permissions = {}
        self._increment = AtomicLong()

        server = Server()
        server.setId(1)
        server.setRegistration(True)
        self._objects[Server.__class__] = { server.getId(): server }

    def getObjects(self, clazz, request):
        return self._objects.computeIfAbsent(clazz, lambda key : {}).values().stream().filter(lambda object : self._checkCondition(request.getCondition(), object)).map(lambda object : object)

    def _checkCondition(self, genericCondition, object):
        if genericCondition is None:
            return True

        if isinstance(genericCondition, Condition.Compare):

            condition = genericCondition
            value = self._retrieveValue(object, condition.getVariable())
            result = (value).compareTo(condition.getValue())
            if condition.getOperator() is "<":
                return result < 0
            elif condition.getOperator() is "<=":
                return result <= 0
            elif condition.getOperator() is ">":
                return result > 0
            elif condition.getOperator() is ">=":
                return result >= 0
            elif condition.getOperator() is "=":
                return result == 0
            else:
                raise RuntimeError("Unsupported comparison condition")

        elif isinstance(genericCondition, Condition.Between):

            condition = genericCondition
            fromValue = self._retrieveValue(object, condition.getFromVariable())
            fromResult = (fromValue).compareTo(condition.getFromValue())
            toValue = self._retrieveValue(object, condition.getToVariable())
            toResult = (toValue).compareTo(condition.getToValue())
            return fromResult >= 0 and toResult <= 0

        elif isinstance(genericCondition, Condition.Binary):

            condition = genericCondition
            if condition.getOperator() is "AND":
                return self._checkCondition(condition.getFirst(), object) and self._checkCondition(condition.getSecond(), object)
            elif condition.getOperator() is "OR":
                return self._checkCondition(condition.getFirst(), object) or self._checkCondition(condition.getSecond(), object)

        elif isinstance(genericCondition, Condition.Permission):

            condition = genericCondition
            id = int(self._retrieveValue(object, "id"))
            #JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
            #            return getPermissionsSet(condition.getOwnerClass(), condition.getPropertyClass()).stream().anyMatch(pair ->
            #            {
            #                        if (condition.getOwnerId() > 0)
            #                        {
            #                            return pair.getFirst() == condition.getOwnerId() && pair.getSecond() == id
            #                        }
            #                        else
            #                        {
            #                            return pair.getFirst() == id && pair.getSecond() == condition.getPropertyId()
            #                        }
            #                    }
            #                    )

        elif isinstance(genericCondition, Condition.LatestPositions):

            return False


        return False

    def _retrieveValue(self, object, key):
        try:
            method = type(object).getMethod("get" + (key[0]).upper() + key[1:])
            return method.invoke(object)
        except RuntimeError as e:
            raise RuntimeError(e)

    def addObject(self, entity, request):
        id = self._increment.incrementAndGet()
        self._objects.computeIfAbsent(type(entity), lambda key : {}).put(id, entity)
        return id

    def updateObject(self, entity, request):
        columns = OrderedDict(request.getColumns().getColumns(type(entity), "get"))
        items = None
        if request.getCondition() is not None:
            id = int((request.getCondition()).getValue())
            items = array(self._objects.computeIfAbsent(type(entity), lambda key : {}).get(id))
        else:
            items = self._objects.computeIfAbsent(type(entity), lambda key : {}).values()
        for setter in type(entity).getMethods():
            if setter.getName().startsWith("set") and setter.getParameterCount() == 1 and columns.contains(setter.getName().lower()):
                try:
                    getter = type(entity).getMethod(setter.getName().replaceFirst("set", "get"))
                    value = getter.invoke(entity)
                    for object in items:
                        setter.invoke(object, value)
                except RuntimeError as e:
                    raise RuntimeError(e)

    def removeObject(self, clazz, request):
        id = int((request.getCondition()).getValue())
        self._objects.computeIfAbsent(clazz, lambda key : {}).remove(id)

    def _getPermissionsSet(self, ownerClass, propertyClass):
        return self._permissions.computeIfAbsent(Pair(ownerClass, propertyClass), lambda k : OrderedDict())

    def getPermissions(self, ownerClass, ownerId, propertyClass, propertyId):
        return self._getPermissionsSet(ownerClass, propertyClass).stream().filter(lambda pair : ownerId == 0 or pair.getFirst() is ownerId).filter(lambda pair : propertyId == 0 or pair.getSecond() is propertyId).map(lambda pair : Permission(ownerClass, pair.getFirst(), propertyClass, pair.getSecond()))

    def addPermission(self, permission):
        self._getPermissionsSet(permission.getOwnerClass(), permission.getPropertyClass()).add(Pair(permission.getOwnerId(), permission.getPropertyId()))

    def removePermission(self, permission):
        self._getPermissionsSet(permission.getOwnerClass(), permission.getPropertyClass()).remove(Pair(permission.getOwnerId(), permission.getPropertyId()))
