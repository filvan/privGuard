from src.examples.program.traccar.config.keys import Keys


class WebHelper:

    def __init__(self):
        pass

    @staticmethod
    def retrieveRemoteAddress(request):

        if request is not None:
            remoteAddress = request.getHeader("X-FORWARDED-FOR")

            if remoteAddress is not None and remoteAddress:
                separatorIndex = remoteAddress.find(",")
                if separatorIndex > 0:
                    return remoteAddress[0:separatorIndex] # remove the additional data
                else:
                    return remoteAddress
            else:
                return request.getRemoteAddr()
        else:
            return None

    @staticmethod
    def retrieveWebUrl(config):
        if config.hasKey(Keys.WEB_URL):
            return config.getString(Keys.WEB_URL).replaceAll("/$", "")
        else:
            address = None
            try:
                address = config.getString(Keys.WEB_ADDRESS, "InetAddress.getLocalHost().getHostAddress()")
            except Exception as e:
                address = "localhost"
            return "URIUtil.newURI(\"http\", address, config.getInteger(Keys.WEB_PORT), "", "")"
