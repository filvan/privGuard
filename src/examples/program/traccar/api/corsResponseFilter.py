from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys


class CorsResponseFilter:

    def __init__(self, config):

        self.allowed = config.getString(Keys.WEB_ORIGIN)

    ORIGIN_ALL = "*"
    HEADERS_ALL = "origin, content-type, accept, authorization"
    METHODS_ALL = "GET, POST, PUT, DELETE, OPTIONS"

    def filter(self, request, response):
        if not response.getHeaders().containsKey(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_HEADERS")):
            response.getHeaders().add(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_HEADERS"),
                                      CorsResponseFilter.HEADERS_ALL)

        if not response.getHeaders().containsKey(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_CREDENTIALS")):
            response.getHeaders().add(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_CREDENTIALS"), True)

        if not response.getHeaders().containsKey(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_METHODS")):
            response.getHeaders().add(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_METHODS"),
                                      CorsResponseFilter.METHODS_ALL)

        if not response.getHeaders().containsKey(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_ORIGIN")):
            origin = request.getHeaderString(str("HttpHeaderNames.ORIGIN"))
            if origin is None:
                response.getHeaders().add(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_ORIGIN"),
                                          CorsResponseFilter.ORIGIN_ALL)
            elif self.allowed is None or self.allowed == CorsResponseFilter.ORIGIN_ALL or origin in self.allowed:
                response.getHeaders().add(str("HttpHeaderNames.ACCESS_CONTROL_ALLOW_ORIGIN"), origin)
