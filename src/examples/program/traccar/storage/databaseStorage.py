

from numpy import array

from .query.columns import Columns
from .query.condition import Condition
from .query.order import Order
from .query.request import Request
from .queryBuilder import QueryBuilder
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.group import Group
from src.examples.program.traccar.model.groupModel import GroupedModel
from src.examples.program.traccar.model.permission import Permission
from .storage import Storage
from .storageException import StorageException
from .storageName import StorageName


class DatabaseStorage(Storage):

    def __init__(self, config, dataSource, objectMapper):

        self._config = None
        self._dataSource = None
        self._objectMapper = None
        self._databaseType = None

        self._config = config
        self._dataSource = dataSource
        self._objectMapper = objectMapper

        try:
            self._databaseType = dataSource.getConnection().getMetaData().getDatabaseProductName()
        except RuntimeError as e:
            raise RuntimeError(e)
    def getObjects(self, clazz, request):
        query = ("SELECT ")
        if isinstance(request.getColumns(), Columns.All):
           query = query +('*')
        else:
            query += (request.getColumns().getColumns(clazz, "set"), lambda c : c)
        query += (" FROM " + Permission.getStorageName(clazz))
        query += request.getCondition()
        query+=(request.getOrder())
        try:
            builder = QueryBuilder.create(self._config, self._dataSource, self._objectMapper, str(query))
            for variable in self._getConditionVariables(request.getCondition()).entrySet():
                builder.setValue(variable.getKey(), variable.getValue())
            return builder.executeQuery(clazz)
        except Exception as e:
            raise Exception(e)
    def addObject(self, entity, request):
        columns = request.getColumns().getColumns(type(entity), "get")
        query = ("INSERT INTO ")
        query += (self._getStorageName(type(entity)))
        query += ("(")
        query += (self._formatColumns(columns, lambda c : c))
        query += (") VALUES (")
        query += (self._formatColumns(columns, lambda c : ':' + c))
        query += (")")
        try:
            builder = QueryBuilder.create(self._config, self._dataSource, self._objectMapper, str(query), True)
            builder.setObject(entity, columns)
            return builder.executeUpdate()
        except Exception as e:
            raise StorageException(e)
    def updateObject(self, entity, request):
        columns = request.getColumns().getColumns(type(entity), "get")
        query  = ("UPDATE ")
        query += (self._getStorageName(type(entity)))
        query += (" SET ")
        query += (self._formatColumns(columns, lambda c : c + " = :" + c))
        query += (self._formatCondition(request.getCondition()))
        try:
            builder = QueryBuilder.create(self._config, self._dataSource, self._objectMapper, str(query))
            builder.setObject(entity, columns)
            for variable in self._getConditionVariables(request.getCondition()).entrySet():
                builder.setValue(variable.getKey(), variable.getValue())
            builder.executeUpdate()
        except Exception as e:
            raise StorageException(e)
    def removeObject(self, clazz, request):
        query = ("DELETE FROM ")
        query += (self._getStorageName(clazz))
        query += (self._formatCondition(request.getCondition()))
        try:
            builder = QueryBuilder.create(self._config, self._dataSource, self._objectMapper, str(query))
            for variable in self._getConditionVariables(request.getCondition()).entrySet():
                builder.setValue(variable.getKey(), variable.getValue())
            builder.executeUpdate()
        except Exception as e:
            raise StorageException(e)

    def getPermissions(self, ownerClass, ownerId, propertyClass, propertyId):
        query = ("SELECT * FROM ")
        query += (Permission.getStorageName(ownerClass, propertyClass))
        conditions = array()
        if ownerId > 0:
            conditions.add(Condition.Equals(Permission.getKey(ownerClass), ownerId))
        if propertyId > 0:
            conditions.add(Condition.Equals(Permission.getKey(propertyClass), propertyId))
        combinedCondition = Condition.merge(conditions)
        query += (self._formatCondition(combinedCondition))
        try:
            builder = QueryBuilder.create(self._config, self._dataSource, self._objectMapper, str(query))
            for variable in self._getConditionVariables(combinedCondition).entrySet():
                builder.setValue(variable.getKey(), variable.getValue())
            return builder.executePermissionsQuery()
        except Exception as e:
            raise StorageException(e)

    def addPermission(self, permission):
        query = ("INSERT INTO ")
        query += (permission.getStorageName())
        query += (" VALUES (")
        query += permission.get().keySet().stream().map(lambda key: ':' + key).join(", ")
        query += (")")
        try:
            builder = QueryBuilder.create(self._config, self._dataSource, self._objectMapper, str(query), True)
            for entry in permission.get().entrySet():
                builder.setLong(entry.getKey(), entry.getValue())
            builder.executeUpdate()
        except Exception as e:
            raise StorageException(e)

    def removePermission(self, permission):
        query = ("DELETE FROM ")
        query += (permission.getStorageName())
        query += (" WHERE ")
        query += (
            permission.get().keySet().stream().map(lambda key: key + " = :" + key).join("AND"))
        try:
            builder = QueryBuilder.create(self._config, self._dataSource, self._objectMapper, str(query), True)
            for entry in permission.get().entrySet():
                builder.setLong(entry.getKey(), entry.getValue())
            builder.executeUpdate()
        except Exception as e:
            raise StorageException(e)

    def _getStorageName(self, clazz):
        storageName = clazz.getAnnotation(StorageName.__class__)
        if storageName is None:

            raise StorageException("StorageName annotation is missing")
        return storageName.value()

    def _getConditionVariables(self, genericCondition):
        results = {}
        if isinstance(genericCondition, Condition.Compare):
            condition = genericCondition
            if condition.getValue() is not None:
                results[condition.getVariable()] = condition.getValue()
        elif isinstance(genericCondition, Condition.Between):
            condition = genericCondition
            results[condition.getFromVariable()] = condition.getFromValue()
            results[condition.getToVariable()] = condition.getToValue()
        elif isinstance(genericCondition, Condition.Binary):
            condition = genericCondition
            results.__setitem__(self._getConditionVariables(condition.getFirst()))
            results.__setitem__(self._getConditionVariables(condition.getSecond()))
        elif isinstance(genericCondition, Condition.Permission):
            condition = genericCondition
            if condition.getOwnerId() > 0:
                results[Permission.getKey(condition.getOwnerClass())] = condition.getOwnerId()
            else:
                results[Permission.getKey(condition.getPropertyClass())] = condition.getPropertyId()
        elif isinstance(genericCondition, Condition.LatestPositions):
            condition = genericCondition
            if condition.getDeviceId() > 0:
                results["deviceId"] = condition.getDeviceId()
        return results

    def _formatColumns(self, columns, mapper):
        return columns.stream().map(mapper).join(", ")

    def _formatCondition(self, genericCondition):
        return self._formatCondition(genericCondition, True)

    def _formatCondition(self, genericCondition, appendWhere):
        result = ""
        if genericCondition is not None:
            if appendWhere:
                result += (" WHERE ")
            if isinstance(genericCondition, Condition.Compare):

                condition = genericCondition
                result += (condition.getColumn())
                result += (" ")
                result += (condition.getOperator())
                result += (" :")
                result += (condition.getVariable())

            elif isinstance(genericCondition, Condition.Between):

                condition = genericCondition
                result += (condition.getColumn())
                result += (" BETWEEN :")
                result += (condition.getFromVariable())
                result += (" AND :")
                result += (condition.getToVariable())

            elif isinstance(genericCondition, Condition.Binary):

                condition = genericCondition
                result += (self._formatCondition(condition.getFirst(), False))
                result += (" ")
                result += (condition.getOperator())
                result += (" ")
                result += (self._formatCondition(condition.getSecond(), False))

            elif isinstance(genericCondition, Condition.Permission):

                condition = genericCondition
                result += ("id IN (")
                result += (self._formatPermissionQuery(condition))
                result += (")")

            elif isinstance(genericCondition, Condition.LatestPositions):

                condition = genericCondition
                result += ("id IN (")
                result += ("SELECT positionId FROM ")
                result += (self._getStorageName(Device.__class__))
                if condition.getDeviceId() > 0:
                    result += (" WHERE id = :deviceId")

                result += (")")

        return str(result)

    def _formatOrder(self, order):
        result = ""
        if order is not None:
            result += (" ORDER BY ")
            result += (order.getColumn())
            if order.getDescending():
                result += (" DESC")
            if order.getLimit() > 0:
                if self._databaseType is "Microsoft SQL Server":
                    result += (" OFFSET 0 ROWS FETCH FIRST ")
                    result += (order.getLimit())
                    result += (" ROWS ONLY")
                else:
                    result += (" LIMIT ")
                    result += (order.getLimit())
        return str(result)

    def _formatPermissionQuery(self, condition):
        result = ""

        outputKey = None
        conditionKey = None
        if condition.getOwnerId() > 0:
            outputKey = Permission.getKey(condition.getPropertyClass())
            conditionKey = Permission.getKey(condition.getOwnerClass())
        else:
            outputKey = Permission.getKey(condition.getOwnerClass())
            conditionKey = Permission.getKey(condition.getPropertyClass())

        storageName = Permission.getStorageName(condition.getOwnerClass(), condition.getPropertyClass())
        result += ("SELECT ")
        result += (storageName) +('.') +(outputKey)
        result += (" FROM ")
        result += (storageName)
        result += (" WHERE ")
        result += (conditionKey)
        result += (" = :")
        result += (conditionKey)

        if condition.getIncludeGroups():

            expandDevices = False
            groupStorageName = None
            if GroupedModel.__subclasscheck__(condition.getOwnerClass()):
                expandDevices = Device.__subclasscheck__(condition.getOwnerClass())

                groupStorageName = Permission.getStorageName(Group.__class__, condition.getPropertyClass())
            else:
                expandDevices = Device.__subclasscheck__(condition.getPropertyClass())

                groupStorageName = Permission.getStorageName(condition.getOwnerClass(), Group.__class__)

            result += (" UNION ")
            result += ("SELECT DISTINCT ")
            if not expandDevices:
                if outputKey == "groupId":
                    result += ("all_groups.")
                else:
                    result += (groupStorageName) + ('.')
            result += (outputKey)
            result += (" FROM ")
            result += (groupStorageName)

            result += (" INNER JOIN (")
            result += ("SELECT id as parentId, id as groupId FROM ")
            result += (self._getStorageName(Group.__class__))
            result += (" UNION ")
            result += ("SELECT groupId as parentId, id as groupId FROM ")
            result += (self._getStorageName(Group.__class__))
            result += (" WHERE groupId IS NOT NULL")
            result += (" UNION ")
            result += ("SELECT g2.groupId as parentId, g1.id as groupId FROM ")
            result += (self._getStorageName(Group.__class__))
            result += (" AS g2")
            result += (" INNER JOIN ")
            result += (self._getStorageName(Group.__class__))
            result += (" AS g1 ON g2.id = g1.groupId")
            result += (" WHERE g2.groupId IS NOT NULL")
            result += (") AS all_groups ON ")
            result += (groupStorageName)
            result += (".groupId = all_groups.parentId")

            if expandDevices:
                result += (" INNER JOIN (")

            result += ("SELECT groupId as parentId, id as deviceId FROM ")
            result += (self._getStorageName(Device.__class__ ))
            result += (" WHERE groupId IS NOT NULL")
            result += (") AS devices ON all_groups.groupId = devices.parentId")

            result += (" WHERE ")
            result += (conditionKey)
            result += (" = :")
            result += (conditionKey)

        return str(result)





