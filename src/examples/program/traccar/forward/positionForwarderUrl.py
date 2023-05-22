import urllib3

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from .positionForwarder import PositionForwarder

from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.helper.checksum import Checksum

import math

class PositionForwarderUrl(PositionForwarder):



    def __init__(self, config, client, objectMapper):

        self._url = None
        self._header = None
        self._client = None
        self._objectMapper = None

        self._client = client
        self._objectMapper = objectMapper
        self._url = config.getString(Keys.FORWARD_URL)
        self._header = config.getString(Keys.FORWARD_HEADER)

    def forward(self, positionData, resultHandler):
        try:
            url = self.formatRequest(positionData)
            requestBuilder = self._client.target(url).request()

            if self._header is not None and self._header:
                for line in self._header.split("\\r?\\n"):
                    values = line.split(":", 2)
                    headerName = values[0].trim()
                    headerValue = values[1].trim()
                    requestBuilder.header(headerName, headerValue)

            requestBuilder.async_().get("InvocationCallbackAnonymousInnerClass(self, resultHandler)")
        except Exception:
            resultHandler.onResult(False, Exception)

    class InvocationCallbackAnonymousInnerClass():


        def __init__(self, outerInstance, resultHandler):
            self._outerInstance = outerInstance
            self._resultHandler = resultHandler

        def completed(self, response):
            if response.getStatusInfo().getFamily() == "Response.Status.Family.SUCCESSFUL":
                self._resultHandler.onResult(True, None)
            else:
                code = response.getStatusInfo().getStatusCode()
                self._resultHandler.onResult(False, Exception("HTTP code " + str(code)))

        def failed(self, throwable):
            self._resultHandler.onResult(False, throwable)



    def formatRequest(self, positionData):

        position = positionData.getPosition()
        device = positionData.getDevice()

        request = self._url.replace("{name}", urllib3.encode(device.getName(), "utf-8")).replace("{uniqueId}", device.getUniqueId()).replace("{status}", device.getStatus()).replace("{deviceId}", str(position.getDeviceId())).replace("{protocol}", str(position.getProtocol())).replace("{deviceTime}", str(position.getDeviceTime().getTime())).replace("{fixTime}", str(position.getFixTime().getTime())).replace("{valid}", str(position.getValid())).replace("{latitude}", str(position.getLatitude())).replace("{longitude}", str(position.getLongitude())).replace("{altitude}", str(position.getAltitude())).replace("{speed}", str(position.getSpeed())).replace("{course}", str(position.getCourse())).replace("{accuracy}", str(position.getAccuracy())).replace("{statusCode}", self._calculateStatus(position))

        if position.getAddress() is not None:
            request = request.replace("{address}", urllib3.encode(position.getAddress(), "utf-8"))

        if "{attributes}" in request:
            attributes = self._objectMapper.writeValueAsString(position.getAttributes())
            request = request.replace("{attributes}", urllib3.encode(attributes, "utf-8"))

        if "{gprmc}" in request:
            request = request.replace("{gprmc}", PositionForwarderUrl._formatSentence(position))

        return request

    @staticmethod
    def _formatSentence(position):

        s = ("$GPRMC,")

        with (s," Locale.ENGLISH") as f:

            calendar = "Calendar.getInstance(TimeZone.getTimeZone(\"UTC\"), Locale.ENGLISH)"
            calendar.setTimeInMillis(position.getFixTime().getTime())

            f.format("%1$tH%1$tM%1$tS.%1$tL,A,", calendar)

            lat = position.getLatitude()
            lon = position.getLongitude()

            f.format("%02d%07.4f,%c,", int(abs(lat)), math.fmod(abs(lat), 1 * 60),'S' if lat < 0 else 'N')
            f.format("%03d%07.4f,%c,", int(abs(lon)), math.fmod(abs(lon), 1 * 60),'W' if lon < 0 else 'E')

            f.format("%.2f,%.2f,", position.getSpeed(), position.getCourse())
            f.format("%1$td%1$tm%1$ty,,", calendar)

        s+=(Checksum.nmea(s.substring(1)))

        return str(s)


    def _calculateStatus(self, position):
        if position.hasAttribute(Position.KEY_ALARM):
            return "0xF841"
        elif position.getSpeed() < 1.0:
            return "0xF020"
        else:
            return "0xF11C"
