from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.configKey import ConfigKey
from src.examples.program.traccar.model.extendedModel import ExtendedModel

class PropertiesProvider:

    def _initialize_instance_fields(self):

        self._config = None
        self._extendedModel = None




    def __init__(self, config):
        self._initialize_instance_fields()

        self._config = config

    def __init__(self, extendedModel):
        self._initialize_instance_fields()

        self._extendedModel = extendedModel

    def getString(self, key):
        if self._config is not None:
            return self._config.getString(key)
        else:
            result = self._extendedModel.getString(key.getKey())
            return result if result is not None else key.getDefaultValue()

    def getInteger(self, key):
        if self._config is not None:
            return self._config.getInteger(key)
        else:
            result = self._extendedModel.getAttributes().get(key.getKey())
            if result is not None:
                return int(str(result)) if isinstance(result, str) else int(result)
            else:
                return key.getDefaultValue()

    def getBoolean(self, key):
        if self._config is not None:
            if self._config.hasKey(key):
                return self._config.getBoolean(key)
            else:
                return None
        else:
            result = self._extendedModel.getAttributes().get(key.getKey())
            if result is not None:
                return bool(str(result)) if isinstance(result, str) else bool(result)
            else:
                return None
