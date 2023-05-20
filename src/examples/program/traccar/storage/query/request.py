class Request:

    def _initialize_instance_fields(self):

        self._columns = None
        self._condition = None
        self._order = None

    def __init__(self, columns):
        self(columns, None, None)

    def __init__(self, condition):
        self(None, condition, None)

    def __init__(self, columns, condition):
        self(columns, condition, None)

    def __init__(self, columns, order):
        self(columns, None, order)

    def __init__(self, columns, condition, order):
        self._initialize_instance_fields()

        self._columns = columns
        self._condition = condition
        self._order = order

    def getColumns(self):
        return self._columns

    def getCondition(self):
        return self._condition

    def getOrder(self):
        return self._order
