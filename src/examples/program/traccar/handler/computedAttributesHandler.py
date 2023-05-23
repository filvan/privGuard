import math
from collections import OrderedDict

from numpy import array

from src.examples.program.traccar.baseDataHandler import BaseDataHandler
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.model.attribute import Attribute
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class ComputedAttributesHandler(BaseDataHandler):

    _LOGGER = "LoggerFactory.getLogger(ComputedAttributesHandler.class)"

    def __init__(self, config, cacheManager):

        self._cacheManager = None
        self._engine = None
        self._features = None
        self._includeDeviceAttributes = False

        self._cacheManager = cacheManager
        sandbox = "JexlSandbox(False)"
        sandbox.allow("com.safe.Functions")
        sandbox.allow(math.__name__)
        self._features = ("JexlFeatures()").localVar(config.getBoolean(Keys.PROCESSING_COMPUTED_ATTRIBUTES_LOCAL_VARIABLES)).loops(config.getBoolean(Keys.PROCESSING_COMPUTED_ATTRIBUTES_LOOPS)).newInstance(config.getBoolean(Keys.PROCESSING_COMPUTED_ATTRIBUTES_NEW_INSTANCE_CREATION)).structuredLiteral(True)
        self._engine = ("JexlBuilder()").strict(True).namespaces("Collections.singletonMap(\"math\", math.__class__)").sandbox(sandbox).create()
        self._includeDeviceAttributes = config.getBoolean(Keys.PROCESSING_COMPUTED_ATTRIBUTES_DEVICE_ATTRIBUTES)

    def _prepareContext(self, position):
        result = OrderedDict()
        if self._includeDeviceAttributes:
            device = self._cacheManager.getObject(Device.__class__, position.getDeviceId())
            if device is not None:
                for key in device.getAttributes().keySet():
                    result.set(key, device.getAttributes().get(key))
        methods = array((type(position).getMethods()))
        [object.__class__.getMethods()]
        for method in methods:
            if method.getName().startsWith("get") and method.getParameterTypes().length == 0:
                name = (method.getName().charAt(3)).casefold() + method.getName().substring(4)

                try:
                    if method.getReturnType() is not map.__class__:
                        result.set(name, method.invoke(position))
                    else:
                        for key in (method.invoke(position)).keys():
                            result.set(str(key), (method.invoke(position))[key])
                except (Exception):
                    ComputedAttributesHandler._LOGGER.warn("Attribute reflection error", Exception)
        return result




    def computeAttribute(self, attribute, position):
        return self._engine.createScript(self._features, self._engine.createInfo(), attribute.getExpression()).execute(self._prepareContext(position))

    def handlePosition(self, position):
        attributes = self._cacheManager.getDeviceObjects(position.getDeviceId(), Attribute.__class__)
        for attribute in attributes:
            if attribute.getAttribute() is not None:
                result = None
                try:
                    result = self.computeAttribute(attribute, position)
                except Exception as error:
                    ComputedAttributesHandler._LOGGER.warn("Attribute computation error", error)
                if result is not None:
                    try:
                        if attribute.getAttribute() is "valid":
                            position.setValid(bool(result))
                        elif attribute.getAttribute() is "latitude":
                            position.setLatitude((result).doubleValue())
                        elif attribute.getAttribute() is "longitude":
                            position.setLongitude((result).doubleValue())
                        elif attribute.getAttribute() is "altitude":
                            position.setAltitude((result).doubleValue())
                        elif attribute.getAttribute() is "speed":
                            position.setSpeed((result).doubleValue())
                        elif attribute.getAttribute() is "course":
                            position.setCourse((result).doubleValue())
                        elif attribute.getAttribute() is "address":
                            position.setAddress(str(result))
                        elif attribute.getAttribute() is "accuracy":
                            position.setAccuracy((result).doubleValue())
                        else:
                            if attribute.getType() is "number":
                                numberValue = result
                                position.getAttributes().put(attribute.getAttribute(), numberValue)
                            elif attribute.getType() is "boolean":
                                booleanValue = bool(result)
                                position.getAttributes().put(attribute.getAttribute(), booleanValue)
                            else:
                                position.getAttributes().put(attribute.getAttribute(), str(result))
                    except Exception as error:
                        ComputedAttributesHandler._LOGGER.warn("Attribute cast error", error)
        return position
