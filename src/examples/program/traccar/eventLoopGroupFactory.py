class EventLoopGroupFactory:

    _bossGroup = "NioEventLoopGroup()"
    _workerGroup = "NioEventLoopGroup()"

    def __init__(self):
        pass

    @staticmethod
    def getBossGroup():
        return EventLoopGroupFactory._bossGroup

    @staticmethod
    def getWorkerGroup():
        return EventLoopGroupFactory._workerGroup
