from .extendedModel import ExtendedModel


class GroupedModel(ExtendedModel):

    def __init__(self):
        # instance fields found by Java to Python Converter:
        super().__init__()
        self._groupId = 0

    def getGroupId(self):
        return self._groupId

    def setGroupId(self, groupId):
        self._groupId = groupId
