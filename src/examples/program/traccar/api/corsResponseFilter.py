from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys

class CorsResponseFilter():


    def __init__(self, config):

        self._allowed = None

        self._allowed = config.getString(Keys.WEB_ORIGIN)

    _ORIGIN_ALL = "*"
    _HEADERS_ALL = "origin, content-type, accept, authorization"
    _METHODS_ALL = "GET, POST, PUT, DELETE, OPTIONS"

    def filter(self, request, response):
        if not response.getHeaders().containsKey(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_HEADERS")):
            response.getHeaders().add(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_HEADERS"), CorsResponseFilter._HEADERS_ALL)

        if not response.getHeaders().containsKey(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_CREDENTIALS")):
            response.getHeaders().add(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_CREDENTIALS"), True)

        if not response.getHeaders().containsKey(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_METHODS")):
            response.getHeaders().add(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_METHODS"), CorsResponseFilter._METHODS_ALL)

        if not response.getHeaders().containsKey(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_ORIGIN")):
            origin = request.getHeaderString(str("HttpHeaderNames.ORIGIN"))
            if origin is None:
                response.getHeaders().add(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_ORIGIN"), CorsResponseFilter._ORIGIN_ALL)
            elif self._allowed is None or self._allowed == CorsResponseFilter._ORIGIN_ALL or origin in self._allowed:
                response.getHeaders().add(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_ORIGIN"), origin)
