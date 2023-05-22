from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from .positionForwarder import PositionForwarder

class PositionForwarderRedis(PositionForwarder):


    def __init__(self, config, objectMapper):
        self._url = None
        self._objectMapper = None

        self._objectMapper = objectMapper
        self._url = config.getString(Keys.FORWARD_URL)

    def forward(self, positionData, resultHandler):

        try:
            key = "positions." + positionData.getDevice().getUniqueId()
            value = self._objectMapper.writeValueAsString(positionData.getPosition())
            with self._url as jedis:
                jedis.lpush(key, value)
            resultHandler.onResult(True, None)
        except Exception as e:
            resultHandler.onResult(False, e)

