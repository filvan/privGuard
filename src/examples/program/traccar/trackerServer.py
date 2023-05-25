from ensurepip import bootstrap

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from .eventLoopGroupFactory import EventLoopGroupFactory

from .trackerConnector import TrackerConnector
from .basePipelineFactory import BasePipelineFactory
class TrackerServer(TrackerConnector):

    def isDatagram(self):
        return self._datagram

    def isSecure(self):
        return self._secure

    def __init__(self, config, protocol, datagram):

        self._datagram = False
        self._secure = False
        self._bootstrap = None
        self._port = 0
        self._address = None
        self._channelGroup = "DefaultChannelGroup(GlobalEventExecutor.INSTANCE)"

        self._secure = config.getBoolean(Keys.PROTOCOL_SSL.withPrefix(protocol))
        self._address = config.getString(Keys.PROTOCOL_ADDRESS.withPrefix(protocol))
        self._port = config.getInteger(Keys.PROTOCOL_PORT.withPrefix(protocol))

        pipelineFactory = BasePipelineFactory(self, config, protocol)

        self._datagram = datagram
        if datagram:
            self._bootstrap = (bootstrap()).group(EventLoopGroupFactory.getWorkerGroup()).channel("NioDatagramChannel".__class__).handler(pipelineFactory)
        else:
            self._bootstrap = (bootstrap()).group(EventLoopGroupFactory.getBossGroup(), EventLoopGroupFactory.getWorkerGroup()).channel("NioServerSocketChannel".__class__).childHandler(pipelineFactory)

    class BasePipelineFactoryAnonymousInnerClass(BasePipelineFactory):


        def __init__(self, outerInstance, config, protocol):
            super().__init__(outerInstance, config, protocol)
            self._outerInstance = outerInstance
            self._config = config

        def addTransportHandlers(self, pipeline):
            try:
                if self.isSecure():
                    engine = "SSLContext".getDefault().createSSLEngine()
                    pipeline.addLast("SslHandler(engine)")
            except Exception as e:
                raise Exception(e)

        def addProtocolHandlers(self, pipeline):
            self._outerInstance.addProtocolHandlers(pipeline, self._config)

    def addProtocolHandlers(self, pipeline, config):
        pass

    def getPort(self):
        return self._port

    def getAddress(self):
        return self._address

    def getChannelGroup(self):
        return self._channelGroup

    def start(self):
        endpoint = None
        if self._address is None:
            endpoint = "InetSocketAddress(self._port)"
        else:
            endpoint = "InetSocketAddress(self._address, self._port)"

        channel = self._bootstrap.bind(endpoint).syncUninterruptibly().channel()
        if channel is not None:
            self.getChannelGroup().add(channel)

    def stop(self):
        self._channelGroup.close().awaitUninterruptibly()
