class CharacterDelimiterFrameDecoder():

    @staticmethod
    def _createDelimiter(delimiter):
        buf = [ord(delimiter)]
        return "Unpooled.wrappedBuffer(buf)"

    @staticmethod
    def _createDelimiter(delimiter):
        buf = [0 for _ in range(len(delimiter))]
        i = 0
        while i < len(delimiter):
            buf[i] = ord(delimiter[i])
            i += 1
        return "Unpooled.wrappedBuffer(buf)"

    @staticmethod
    def _convertDelimiters(delimiters):
        result = [None for _ in range(len(delimiters))]
        i = 0
        while i < len(delimiters):
            result[i] = CharacterDelimiterFrameDecoder._createDelimiter(delimiters[i])
            i += 1
        return result

    def __init__(self, maxFrameLength, delimiter):
        super().__init__(maxFrameLength, CharacterDelimiterFrameDecoder._createDelimiter(delimiter))

    def __init__(self, maxFrameLength, delimiter):
        super().__init__(maxFrameLength, CharacterDelimiterFrameDecoder._createDelimiter(delimiter))

    def __init__(self, maxFrameLength, stripDelimiter, delimiter):
        super().__init__(maxFrameLength, stripDelimiter, CharacterDelimiterFrameDecoder._createDelimiter(delimiter))

    def __init__(self, maxFrameLength, *delimiters):
        super().__init__(maxFrameLength, CharacterDelimiterFrameDecoder._convertDelimiters(delimiters))

    def __init__(self, maxFrameLength, stripDelimiter, *delimiters):
        super().__init__(maxFrameLength, stripDelimiter, CharacterDelimiterFrameDecoder._convertDelimiters(delimiters))
