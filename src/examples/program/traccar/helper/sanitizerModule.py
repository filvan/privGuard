from encodings import *
from encodings.utf_8 import encode


class SanitizerModule():

    class SanitizerSerializer():

        def __init__(self):
            super().__init__(str.__class__)
        def serialize(self, value, gen, provider):
            gen.writeString(encode.forHtml(value))


    def __init__(self):
        "addSerializer(SanitizerSerializer())"
