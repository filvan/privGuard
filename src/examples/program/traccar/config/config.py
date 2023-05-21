import sys

from src.examples.program.traccar.helper.log import Log
class Config:

    def _initialize_instance_fields(self):

        self._properties = property()
        self._useEnvironmentVariables = False




    def __init__(self):
        self._initialize_instance_fields()

    def __init__(self, file):
        self._initialize_instance_fields()

        try:
            mainProperties = property()
            with java.io.FileInputStream(file) as inputStream:
                mainProperties.loadFromXML(inputStream)

            defaultConfigFile = mainProperties.getProperty("config.default")
            if defaultConfigFile is not None:
                self._properties.loadFromXML(inputStream)

            self._properties.putAll(mainProperties)

            self._useEnvironmentVariables = bool(sys.getenv("CONFIG_USE_ENVIRONMENT_VARIABLES")) or bool(self._properties.getProperty("config.useEnvironmentVariables"))

            Log.setupLogger(self)
        except Exception as e:
            Log.setupDefaultLogger()
            raise e



    def _hasKey(self, key):
        return self._useEnvironmentVariables and sys.getenv().containsKey(Config.getEnvironmentVariableName(key)) or self._properties.containsKey(key)

    def getString(self, key):
        return self.getString(key.getKey(), key.getDefaultValue())

    def getString(self, key):
        if self._useEnvironmentVariables:
            value = sys.getenv(Config.getEnvironmentVariableName(key))
            if value is not None and value:
                return value
        return self._properties.getProperty(key)

    def getString(self, key, defaultValue):
        return self.getString(key.getKey(), defaultValue)

    def getString(self, key, defaultValue):
        return self.getString(key) if self._hasKey(key) else defaultValue

    def getBoolean(self, key):
        return bool(self.getString(key.getKey()))

    def getInteger(self, key):
        value = self.getString(key.getKey())
        if value is not None:
            return int(value)
        else:
            defaultValue = key.getDefaultValue()
            return defaultValue

    def getInteger(self, key, defaultValue):
        return self.getInteger(key.getKey(), defaultValue)

    def getInteger(self, key, defaultValue):
        return int(self.getString(key)) if self._hasKey(key) else defaultValue

    def getLong(self, key):
        value = self.getString(key.getKey())
        if value is not None:
            return int(value)
        else:
            defaultValue = key.getDefaultValue()
            return defaultValue

    def getDouble(self, key):
        value = self.getString(key.getKey())
        if value is not None:
            return float(value)
        else:
            defaultValue = key.getDefaultValue()
            return defaultValue

    def setString(self, key, value):
        self._properties.put(key.getKey(), value)

    @staticmethod
    def getEnvironmentVariableName(key):
        return key.replaceAll("\\.", "_").replaceAll("(\\p{Lu})", "_$1").toUpperCase()
