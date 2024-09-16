class Order:

    def _initialize_instance_fields(self):
        self._column = None
        self._descending = False
        self._limit = 0

    def __init__(self, column):
        self(column, False, 0)

    def __init__(self, column, descending, limit):
        self._initialize_instance_fields()

        self._column = column
        self._descending = descending
        self._limit = limit

    def getColumn(self):
        return self._column

    def getDescending(self):
        return self._descending
