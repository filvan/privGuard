import this

from src.examples.program.traccar.model.groupModel import GroupedModel


class Condition:
    def merge(self, conditions):
        result = None
        iterator = conditions.iterator()
        if iterator.hasNext():
            result = iterator.next()
            while iterator.hasNext():
                result = Condition.And(self, result, iterator.next())
        return result

    class Equals(this.Compare):

        def __init__(self, outerInstance, column, value):
            super().__init__(outerInstance, column, "=", column, value)
            self._outerInstance = outerInstance

    class Compare(this.Condition):

        def __init__(self, outerInstance, column, operator, variable, value):
            self._column = None
            self._operator = None
            self._variable = None
            self._value = None

            self._outerInstance = outerInstance

            self._column = column
            self._operator = operator
            self._variable = variable
            self._value = value

        def getColumn(self):
            return self._column

        def getOperator(self):
            return self._operator

        def getVariable(self):
            return self._variable

        def getValue(self):
            return self._value

    class Between(this.Condition):

        def __init__(self, outerInstance, column, fromVariable, fromValue, toVariable, toValue):
            self._column = None
            self._fromVariable = None
            self._fromValue = None
            self._toVariable = None
            self._toValue = None

            self._outerInstance = outerInstance

            self._column = column
            self._fromVariable = fromVariable
            self._fromValue = fromValue
            self._toVariable = toVariable
            self._toValue = toValue

        def getColumn(self):
            return self._column

        def getFromVariable(self):
            return self._fromVariable

        def getFromValue(self):
            return self._fromValue

        def getToVariable(self):
            return self._toVariable

        def getToValue(self):
            return self._toValue

    class Or(this.Binary):

        def __init__(self, outerInstance, first, second):
            super().__init__(outerInstance, first, second, "OR")
            self._outerInstance = outerInstance

    class And(this.Binary):

        def __init__(self, outerInstance, first, second):
            super().__init__(outerInstance, first, second, "AND")
            self._outerInstance = outerInstance

    class Binary(this.Condition):

        def __init__(self, outerInstance, first, second, operator):
            self._first = None
            self._second = None
            self._operator = None

            self._outerInstance = outerInstance

            self._first = first
            self._second = second
            self._operator = operator

        def getFirst(self):
            return self._first

        def getSecond(self):
            return self._second

        def getOperator(self):
            return self._operator

    class Permission(this.Condition):

        def _initialize_instance_fields(self):
            self._ownerClass = None
            self._ownerId = 0
            self._propertyClass = None
            self._propertyId = 0
            self._excludeGroups = False

        def __init__(self, ownerClass, ownerId, propertyClass, propertyId, excludeGroups):
            self._initialize_instance_fields()

            self._ownerClass = ownerClass
            self._ownerId = ownerId
            self._propertyClass = propertyClass
            self._propertyId = propertyId
            self._excludeGroups = excludeGroups

        def __init__(self, ownerClass, ownerId, propertyClass):
            self(ownerClass, ownerId, propertyClass, 0, False)

        def __init__(self, ownerClass, propertyClass, propertyId):
            self(ownerClass, 0, propertyClass, propertyId, False)

        def excludeGroups(self):
            return this.Permission(self._ownerClass, self._ownerId, self._propertyClass, self._propertyId, True)

        def getOwnerClass(self):
            return self._ownerClass

        def getOwnerId(self):
            return self._ownerId

        def getPropertyClass(self):
            return self._propertyClass

        def getPropertyId(self):
            return self._propertyId

        def getIncludeGroups(self):
            ownerGroupModel = GroupedModel.__class__.isAssignableFrom(self._ownerClass)

            propertyGroupModel = GroupedModel.__class__.isAssignableFrom(self._propertyClass)

            return (ownerGroupModel or propertyGroupModel) and not self._excludeGroups

    class LatestPositions(this.Condition):

        def _initialize_instance_fields(self):
            self._deviceId = 0

        def __init__(self, deviceId):
            self._initialize_instance_fields()

            self._deviceId = deviceId

        def __init__(self):
            self(0)

        def getDeviceId(self):
            return self._deviceId
