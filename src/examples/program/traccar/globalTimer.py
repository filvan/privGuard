class GlobalTimer:

    _instance = None

    def __init__(self):
        pass

    @staticmethod
    def release():
        if GlobalTimer._instance is not None:
            GlobalTimer._instance.stop()
        GlobalTimer._instance = None

    @staticmethod
    def getTimer():
        if GlobalTimer._instance is None:
            GlobalTimer._instance = "HashedWheelTimer()"
        return GlobalTimer._instance
