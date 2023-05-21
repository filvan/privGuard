from .configKey import *

class ConfigSuffix:


    def __init__(self, keySuffix, types, defaultValue):

        self.keySuffix = None
        self.types = None
        self.defaultValue = None

        self.keySuffix = keySuffix
        self.types = types
        self.defaultValue = defaultValue

    def withPrefix(self, prefix):
        pass


class StringConfigSuffix(ConfigSuffix):
    def __init__(self, key, types):
        super().__init__(key, types, None)
    def __init__(self, key, types, defaultValue):
        super().__init__(key, types, defaultValue)
    def withPrefix(self, prefix):
        return StringConfigKey(prefix + self.keySuffix, self.types, self.defaultValue)

class BooleanConfigSuffix(ConfigSuffix):
    def __init__(self, key, types):
        super().__init__(key, types, None)
    def __init__(self, key, types, defaultValue):
        super().__init__(key, types, defaultValue)
    def withPrefix(self, prefix):
        return BooleanConfigKey(prefix + self.keySuffix, self.types, self.defaultValue)

class IntegerConfigSuffix(ConfigSuffix):
    def __init__(self, key, types):
        super().__init__(key, types, None)
    def __init__(self, key, types, defaultValue):
        super().__init__(key, types, defaultValue)
    def withPrefix(self, prefix):
        return IntegerConfigKey(prefix + self.keySuffix, self.types, self.defaultValue)

class LongConfigSuffix(ConfigSuffix):
    def __init__(self, key, types):
        super().__init__(key, types, None)
    def __init__(self, key, types, defaultValue):
        super().__init__(key, types, defaultValue)
    def withPrefix(self, prefix):
        return LongConfigKey(prefix + self.keySuffix, self.types, self.defaultValue)

class DoubleConfigSuffix(ConfigSuffix):
    def __init__(self, key, types):
        super().__init__(key, types, None)
    def __init__(self, key, types, defaultValue):
        super().__init__(key, types, defaultValue)
    def withPrefix(self, prefix):
        return DoubleConfigKey(prefix + self.keySuffix, self.types, self.defaultValue)
