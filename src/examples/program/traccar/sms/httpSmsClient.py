from xml.dom.minidom import Entity

from django.http.request import MediaType

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.helper.dataConvereter import DataConverter
from src.examples.program.traccar.notification.messageException import MessageException
from src.examples.program.traccar.sms.smsManager import SmsManager


class HttpSmsClient(SmsManager):


    def __init__(self, config, client):

        self._client = None
        self._url = None
        self._authorizationHeader = None
        self._authorization = None
        self._template = None
        self._encode = False
        self._mediaType = None

        self._client = client
        self._url = config.getString(Keys.SMS_HTTP_URL)
        self._authorizationHeader = config.getString(Keys.SMS_HTTP_AUTHORIZATION_HEADER)
        if config.hasKey(Keys.SMS_HTTP_AUTHORIZATION):
            self._authorization = config.getString(Keys.SMS_HTTP_AUTHORIZATION)
        else:
            user = config.getString(Keys.SMS_HTTP_USER)
            password = config.getString(Keys.SMS_HTTP_PASSWORD)
            if user is not None and password is not None:
                self._authorization = "Basic " + DataConverter.printBase64((user + ":" + password).getBytes('utf-8'))
            else:
                self._authorization = None
        self._template = config.getString(Keys.SMS_HTTP_TEMPLATE).trim()
        if self._template[0] == '{' or self._template[0] == '[':
            self._encode = False
            self._mediaType = MediaType.APPLICATION_JSON_TYPE
        else:
            self._encode = True
            self._mediaType = MediaType.APPLICATION_FORM_URLENCODED_TYPE

    def _prepareValue(self, value):
        return "URLEncoder.encode(value, StandardCharsets.UTF_8)" if self._encode else value

    def _preparePayload(self, destAddress, message):
        try:
            return self._template.replace("{phone}", self._prepareValue(destAddress)).replace("{message}", self._prepareValue(message.trim()))
        except Exception as e:
            raise Exception(e)

    def _getRequestBuilder(self):
        builder = self._client.target(self._url).request()
        if self._authorization is not None:
            builder = builder.header(self._authorizationHeader, self._authorization)
        return builder

    def sendMessage(self, destAddress, message, command):
        with self._getRequestBuilder().post(Entity.entity(self._preparePayload(destAddress, message), self._mediaType)) as response:
            if response.getStatus() / 100 != 2:
                raise MessageException(response.readEntity(str.__class__))
