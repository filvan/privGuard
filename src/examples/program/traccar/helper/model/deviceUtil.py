import collections

from numpy import array

from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.group import Group
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request


class DeviceUtil:

    def __init__(self):
        pass


    def resetStatus(storage):
        storage.updateObject(Device(), Request(Columns.Include("status")))


    def getAccessibleDevices(storage, userId, deviceIds, groupIds):

        devices = storage.getObjects(Device.__class__, Request(Columns.All(), Condition.Permission(User.__class__, userId, Device.__class__)))
        deviceById = devices.stream().collect(collections.toUnmodifiableMap(Device.getId(), lambda x : x))
        devicesByGroup = devices.stream().filter(lambda x : x.getGroupId() > 0).collect(collections.groupingBy(Device.getGroupId))

        groups = storage.getObjects(Group.__class__, Request(Columns.All(), Condition.Permission(User.__class__, userId, Group.__class__)))
        groupsByGroup = groups.stream().filter(lambda x : x.getGroupId() > 0).collect(collections.groupingBy(Group.getGroupId))

        results = deviceIds.stream().map(deviceById.get()).filter().collect(collections.toSet())

        groupQueue = array(groupIds)
        while not groupQueue.isEmpty():
            groupId = groupQueue.pop()
            results.addAll(devicesByGroup.getOrDefault(groupId, collections.emptyList()))
            groupQueue.__add__(groupsByGroup.getOrDefault(groupId, collections.emptyList()).stream().map(Group.getId).collect(collections.toUnmodifiableList()))

        return results
