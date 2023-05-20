from src.examples.program.traccar.helper.classScanner import ClassScanner
from .baseModel import BaseModel
import collections
class Permission:

    def _initialize_instance_fields(self):

        self._data = None
        self._ownerClass = None
        self._ownerId = 0
        self._propertyClass = None
        self._propertyId = 0


    _CLASSES =collections.ChainMap({},{})

    @staticmethod
    def _static_initializer():
        for clazz in ClassScanner.findSubclasses(BaseModel.__class__):
                Permission._CLASSES[clazz.__name__] = clazz

    _static_initializer()




    def __init__(self, data):
        self._initialize_instance_fields()

        self._data = data
        iterator = data.entrySet().iterator()
        owner = iterator.next()
        self._ownerClass = Permission.getKeyClass(owner.getKey())
        self._ownerId = owner.getValue()
        property = iterator.next()
        self._propertyClass = Permission.getKeyClass(property.getKey())
        self._propertyId = property.getValue()



    def __init__(self, ownerClass, ownerId, propertyClass, propertyId):
        self._initialize_instance_fields()

        self._ownerClass = ownerClass
        self._ownerId = ownerId
        self._propertyClass = propertyClass
        self._propertyId = propertyId
        self._data = collections.OrderedDict()
        self._data.put(Permission.getKey(ownerClass), ownerId)
        self._data.put(Permission.getKey(propertyClass), propertyId)

    @staticmethod
    def getKeyClass(key):
        return Permission._CLASSES[key[0:len(key) - 2]]

    @staticmethod
    def getKey(clazz):
        return clazz.__name__.lower() + "Id"

    @staticmethod

    def getStorageName(ownerClass, propertyClass):
        ownerName = ownerClass.__name__
        propertyName = propertyClass.__name__
        managedPrefix = "Managed"
        if propertyName.startswith(managedPrefix):
            propertyName = propertyName[len(managedPrefix):]
        return "tc_" + ownerName.lower() + "_" + propertyName.lower()




    def getStorageName(self):
        return Permission.getStorageName(self._ownerClass, self._propertyClass)



    def get(self):
        return self._data



    def set(self, key, value):
        self._data.put(key, value)



    def getOwnerClass(self):
        return self._ownerClass



    def getOwnerId(self):
        return self._ownerId



    def getPropertyClass(self):
        return self._propertyClass



    def getPropertyId(self):
        return self._propertyId
