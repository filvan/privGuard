from kafka import KafkaProducer
from pandas.core.indexes.accessors import Properties

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys

from .positionForwarder import PositionForwarder
class PositionForwarderKafka(PositionForwarder):



    def __init__(self, config, objectMapper):
        #instance fields found by Java to Python Converter:
        self._producer = None
        self._objectMapper = None
        self._topic = None

        self._objectMapper = objectMapper
        properties = Properties()
        properties.put("bootstrap.servers", config.getString(Keys.FORWARD_URL))
        properties.put("acks", "all")
        properties.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer")
        properties.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer")
        self._producer = KafkaProducer(properties)
        self._topic = config.getString(Keys.FORWARD_TOPIC)

    def forward(self, positionData, resultHandler):
        try:
            key = str(positionData.getDevice().getId())
            value = self._objectMapper.writeValueAsString(positionData)
            self._producer.send("ProducerRecord(self._topic, key, value)")
            resultHandler.onResult(True, None)
        except Exception as e:
            resultHandler.onResult(False, e)
