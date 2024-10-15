class Pair:

    def __init__(self, first, second):

        self._first = None
        self._second = None

        self._first = first
        self._second = second

    def getFirst(self):
        return self._first

    def getSecond(self):
        return self._second

    def equals(self, o):
        if self is o:
            return True
        if o is None or self.__class__ != type(o):
            return False

        pair = o

        return self._first == pair._first and self._second == pair._second

    # def hashCode(self):
    #   return Objects.hash(self._first, self._second)
