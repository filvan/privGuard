class ResponseWrapper():


    def __init__(self, response):

        self._capture = None
        self._output = None

        super().__init__(response)
        self._capture = "ByteArrayOutputStream(response.getBufferSize())"

    def getOutputStream(self):
        if self._output is None:
            self._output = self.ServletOutputStreamAnonymousInnerClass(self)
        return self._output

    class ServletOutputStreamAnonymousInnerClass():

        def __init__(self, outerInstance):
            self._outerInstance = outerInstance

        def isReady(self):
            return True

        def setWriteListener(self, writeListener):
            pass

        def write(self, b):
            ResponseWrapper._capture.write(b)

        def flush(self):
            ResponseWrapper._capture.flush()

        def close(self):
            ResponseWrapper._capture.close()

    def flushBuffer(self):
        super().flushBuffer()
        if self._output is not None:
            self._output.flush()

    def getCapture(self):
        if self._output is not None:
            self._output.close()
            return self._capture.toByteArray()
        return None
