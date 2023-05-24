from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.group import Group

class GroupTree:

    class TreeNode:

        def _initialize_instance_fields(self):

            self._group = None
            self._device = None
            self._children = set()



        def __init__(self, group):
            self._initialize_instance_fields()

            self._group = group

        def __init__(self, device):
            self._initialize_instance_fields()

            self._device = device

        def hashCode(self):
            if self._group is not None:
                return int(self._group.getId())
            else:
                return int(self._device.getId())

        def equals(self, obj):
            if not(isinstance(obj, self.TreeNode.__class__)):
                return False
            other = obj
            if other is self:
                return True
            if self._group is not None and other._group is not None:
                return self._group.getId() == other._group.getId()
            elif self._device is not None and other._device is not None:
                return self._device.getId() == other._device.getId()
            return False

        def getGroup(self):
            return self._group

        def getDevice(self):
            return self._device

        def setParent(self, parent):
            if parent is not None:
                parent._children.add(self)

        def getChildren(self):
            return self._children



    def __init__(self, groups, devices):

        self._groupMap = {}


        for group in groups:
            self._groupMap[group.getId()] = self.TreeNode(group)

        for node in self._groupMap.values():
            if node.getGroup().getGroupId() != 0:
                node.setParent(self._groupMap[node.getGroup().getGroupId()])

        deviceMap = {}

        for device in devices:
            deviceMap[device.getId()] = self.TreeNode(device)

        for node in deviceMap.values():
            if node.getDevice().getGroupId() != 0:
                node.setParent(self._groupMap[node.getDevice().getGroupId()])


    def getGroups(self, groupId):
        results = set()
        self._getNodes(results, self._groupMap[groupId])
        groups = []
        for node in results:
            if node.getGroup() is not None:
                groups.add(node.getGroup())
        return groups

    def getDevices(self, groupId):
        results = set()
        self._getNodes(results, self._groupMap[groupId])
        devices = []
        for node in results:
            if node.getDevice() is not None:
                devices.add(node.getDevice())
        return devices

    def _getNodes(self, results, node):
        if node is not None:
            for child in node.getChildren():
                results.add(child)
                self._getNodes(results, child)
