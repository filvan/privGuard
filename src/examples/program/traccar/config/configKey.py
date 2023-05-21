from hs import HashSet

class ConfigKey:


    def __init__(self, key, types, valueClass, defaultValue):

        self._key = None
        self._types = HashSet()
        self._valueClass = None
        self._defaultValue = None

        self._key = key
        self._types.addAll(types)
        self._valueClass = valueClass
        self._defaultValue = defaultValue

    def getKey(self):
        return self._key

    def hasType(self, type):
        return self._types.contains(type)

    def getValueClass(self):
        return self._valueClass

    def getDefaultValue(self):
        return self._defaultValue


class StringConfigKey(ConfigKey):
    def __init__(self, key, types):
        super().__init__(key, types,str.__class__, None)
    def __init__(self, key, types, defaultValue):
        super().__init__(key, types, str.__class__, defaultValue)

class BooleanConfigKey(ConfigKey):
    def __init__(self, key, types):
        super().__init__(key, types, bool.__class__, None)
    def __init__(self, key, types, defaultValue):
        super().__init__(key, types, bool.__class__, defaultValue)

class IntegerConfigKey(ConfigKey):
    def __init__(self, key, types):
        super().__init__(key, types, int.__class__, None)
    def __init__(self, key, types, defaultValue):
        super().__init__(key, types, int.__class__, defaultValue)

class LongConfigKey(ConfigKey):
    def __init__(self, key, types):
        super().__init__(key, types, float.__class__, None)
    def __init__(self, key, types, defaultValue):
        super().__init__(key, types, float.__class__, defaultValue)

class DoubleConfigKey(ConfigKey):
    def __init__(self, key, types):
        super().__init__(key, types, float.__class__, None)
    def __init__(self, key, types, defaultValue):
        super().__init__(key, types, float.__class__, defaultValue)
