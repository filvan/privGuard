import this
from array import array
from src.examples.program.traccar.storage.queryIgnore import QueryIgnore


class Columns:

    def getColumns(self, clazz, type):
        pass

    def getAllColumns(self, clazz, type):
        columns = array()
        methods = clazz.getMethods()
        for method in methods:
            parameterCount = 1 if type == "set" else 0
            if method.getName().startsWith(type) and method.getParameterTypes().length == parameterCount and (
            not method.isAnnotationPresent(QueryIgnore.__class__)) and method.getName() is not "getClass":
                columns.append(method.getName().substring(3).lower())
        return columns

    class All(this.Columns):
        def getColumns(self, clazz, type):
            return self.getAllColumns(clazz, type)

    class Include(this.Columns):

        def __init__(self, *columns):
            self._columns = None

            self._columns = array(columns)

        def getColumns(self, clazz, type):
            return self._columns

    class Exclude(this.Columns):

        def __init__(self, *columns):
            self._columns = None

            self._columns = array(columns)

        def getColumns(self, clazz, type):
            return self.getAllColumns(clazz, type).stream().filter(lambda column: (not self._columns.contains(column)))
