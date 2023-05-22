class ObjectMapperContextResolver():
    def __init__(self, objectMapper):
        #instance fields found by Java to Python Converter:
        self._objectMapper = None

        self._objectMapper = objectMapper

    def getContext(self, clazz):
        return self._objectMapper
