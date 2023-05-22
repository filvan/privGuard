from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.configKey import ConfigKey
from src.examples.program.traccar.config.keyType import KeyType
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.group import Group
from src.examples.program.traccar.model.server import Server
from src.examples.program.traccar.session.cache.cacheManager import CacheManager
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class AttributeUtil:

    def __init__(self):
        pass

    class Provider:
        def getDevice(self):
            pass
        def getGroup(self, groupId):
            pass
        def getServer(self):
            pass
        def getConfig(self):
            pass

    @staticmethod

    def lookup(cacheManager, key, deviceId):
        return AttributeUtil.lookup("CacheProvider(cacheManager, deviceId)", key)

    @staticmethod



    def lookup(provider, key):
        device = provider.getDevice()
        result = device.getAttributes().get(key.getKey())
        groupId = device.getGroupId()
        while result is None and groupId > 0:
            group = provider.getGroup(groupId)
            if group is not None:
                result = group.getAttributes().get(key.getKey())
                groupId = group.getGroupId()
            else:
                groupId = 0
        if result is None and key.hasType(KeyType.SERVER):
            result = provider.getServer().getAttributes().get(key.getKey())
        if result is None and key.hasType(KeyType.CONFIG):
            result = provider.getConfig().getString(key.getKey())

        if result is not None:
            valueClass = key.getValueClass()
            if valueClass is bool.__class__:
                return (bool(str(result)) if isinstance(result, str) else result)
            elif valueClass is int.__class__:
                return (int(str(result)) if isinstance(result, str) else (result).intValue())
            elif valueClass is int.__class__:
                return (int(str(result)) if isinstance(result, str) else (result).longValue())
            elif valueClass is float.__class__:
                return (float(str(result)) if isinstance(result, str) else (result).doubleValue())
            else:
                return result
        return key.getDefaultValue()

    @staticmethod
    def getDevicePassword(cacheManager, deviceId, protocol, defaultPassword):

        password = AttributeUtil.lookup(cacheManager, Keys.DEVICE_PASSWORD, deviceId)
        if password is not None:
            return password

        if protocol is not None:
            password = cacheManager.getConfig().getString(Keys.PROTOCOL_DEVICE_PASSWORD.withPrefix(protocol))
            if password is not None:
                return password

        return defaultPassword

    class CacheProvider(Provider):


        def __init__(self, cacheManager, deviceId):

            self._cacheManager = None
            self._deviceId = 0

            self._cacheManager = cacheManager
            self._deviceId = deviceId

        def getDevice(self):
            return self._cacheManager.getObject(Device.__class__, self._deviceId)

        def getGroup(self, groupId):
            return self._cacheManager.getObject(Group.__class__, groupId)

        def getServer(self):
            return self._cacheManager.getServer()

        def getConfig(self):
            return self._cacheManager.getConfig()

    class StorageProvider(Provider):


        def __init__(self, config, storage, permissionsService, device):

            self._config = None
            self._storage = None
            self._permissionsService = None
            self._device = None

            self._config = config
            self._storage = storage
            self._permissionsService = permissionsService
            self._device = device

        def getDevice(self):
            return self._device

        def getGroup(self, groupId):
            try:
                return self._storage.getObject(Group.__class__, Request(Columns.All(), Condition.Equals("id", groupId)))
            except StorageException as e:
                raise Exception(e)

        def getServer(self):
            try:
                return self._permissionsService.getServer()
            except StorageException as e:
                raise Exception(e)

        def getConfig(self):
            return self._config
