class BaseModel:

    def __init__(self):
        # instance fields found by Java to Python Converter:
        self._id = 0

    def getId(self):
        return self._id

    def setId(self, id):
        self._id = id
