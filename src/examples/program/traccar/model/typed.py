class Typed:


    def __init__(self, type):
        #instance fields found by Java to Python Converter:
        self._type = None

        self._type = type

    def getType(self):
        return self._type

    def setType(self, type):
        self._type = type

    def equals(self, o):
        if self is o:
            return True
        if o is None or o.__class__ != type(o):
            return False
        return self._type == (o)._type


