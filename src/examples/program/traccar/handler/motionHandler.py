from src.examples.program.traccar.baseDataHandler import BaseDataHandler
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.helper.model.attributeUtil import AttributeUtil
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class MotionHandler(BaseDataHandler):

    def __init__(self, cacheManager):

        self._cacheManager = None

        self._cacheManager = cacheManager

    def handlePosition(self, position):
        if not position.hasAttribute(Position.KEY_MOTION):
            threshold = AttributeUtil.lookup(self._cacheManager, Keys.EVENT_MOTION_SPEED_THRESHOLD, position.getDeviceId())
            position.set(Position.KEY_MOTION, position.getSpeed() > threshold)
        return position
