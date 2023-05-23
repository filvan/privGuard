from src.examples.program.traccar.baseDataHandler import BaseDataHandler
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.helper.model.attributeUtil import AttributeUtil
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class CopyAttributesHandler(BaseDataHandler):


    def __init__(self, config, cacheManager):

        self._enabled = False
        self._cacheManager = None

        self._enabled = config.getBoolean(Keys.PROCESSING_COPY_ATTRIBUTES_ENABLE)
        self._cacheManager = cacheManager

    def handlePosition(self, position):
        if self._enabled:
            attributesString = AttributeUtil.lookup(self._cacheManager, Keys.PROCESSING_COPY_ATTRIBUTES, position.getDeviceId())
            last = self._cacheManager.getPosition(position.getDeviceId())
            if last is not None and attributesString is not None:
                for attribute in attributesString.split("[ ,]"):
                    if last.hasAttribute(attribute) and not position.hasAttribute(attribute):
                        position.getAttributes().put(attribute, last.getAttributes().get(attribute))
        return position
