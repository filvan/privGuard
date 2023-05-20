

class ClassScanner:

    def __init__(self):
        pass

    @staticmethod



    def findSubclasses(baseClass):
        return set(baseClass.__subclasses__()).union([s for c in baseClass.__subclasses__() for s in ClassScanner.findSubclasses(c)])




