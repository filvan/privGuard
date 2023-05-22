import base64


class DataConverter:

    def __init__(self):
        pass

    @staticmethod
    def parseHex(string):
        try:
            return hex.decodeHex(string)
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def printHex(data):
        return hex.encodeHexString(data)

    @staticmethod
    def parseBase64(string):
        return base64.decodeBase64(string)

    @staticmethod
    def printBase64(data):
        return base64.encodeBase64String(data)
