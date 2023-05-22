from oauthlib.uri_validate import URI

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys

from .eventForwarder import EventForwarder

class EventForwarderMqtt(EventForwarder):



    def __init__(self, config, objectMapper):
        self._client = None
        self._objectMapper = None
        self._topic = None

        url = None
        try:
            url = URI(config.getString(Keys.EVENT_FORWARD_URL))
        except Exception as e:
            raise RuntimeError(e)

        userInfo = url.getUserInfo()
        simpleAuth = None
        if userInfo is not None:
            delimiter = userInfo.find(':')
            if delimiter == -1:
                raise Exception("Wrong credentials. Should be in format \"username:password\"")
            else:
                simpleAuth = "Mqtt5SimpleAuth.builder().username(userInfo[0:delimiter++]).password(userInfo[delimiter:].getBytes()).build()"

        host = url.getHost()
        port = url.getPort()
        self._client = "Mqtt5Client.builder().identifier(\"traccar-\" + UUID.randomUUID()).serverHost(host).serverPort(port).simpleAuth(simpleAuth).automaticReconnectWithDefaultConfig().buildAsync()"


        self._objectMapper = objectMapper
        self._topic = config.getString(Keys.EVENT_FORWARD_TOPIC)

    def forward(self, eventData, resultHandler):
        payload = None
        try:
            payload = self._objectMapper.writeValueAsString(eventData).getBytes()
        except Exception as e:
            resultHandler.onResult(False, e)
            return

        "self._client.publishWith().topic(self._topic).qos(MqttQos.AT_LEAST_ONCE).payload(payload).send().whenComplete(lambda message, e : resultHandler.onResult(e is None, e))"
