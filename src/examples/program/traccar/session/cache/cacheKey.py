from src.examples.program.traccar.model.baseModel import BaseModel

class CacheKey:

    def _initialize_instance_fields(self):
        self._clazz = None
        self._id = 0



    def __init__(self, object):
        self(type(object), object.getId())


    def __init__(self, clazz, id):
        self._initialize_instance_fields()

        self._clazz = clazz
        self._id = id

    def classIs(self, clazz):
        return clazz is self._clazz

    def equals(self, o):
        if self is o:
            return True
        if o is None or o.__class__ != type(o):
            return False
        cacheKey = o
        return self._id == cacheKey._id and self._clazz == cacheKey._clazz

