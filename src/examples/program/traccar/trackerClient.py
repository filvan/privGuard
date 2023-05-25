from ssl import SSLContext

from src.examples.program.traccar.basePipelineFactory import BasePipelineFactory
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.eventLoopGroupFactory import EventLoopGroupFactory
from src.examples.program.traccar.trackerConnector import TrackerConnector


class TrackerClient(TrackerConnector):

    def isDatagram(self):
        return False

    def isSecure(self):
        return self._secure

    def __init__(self, config, protocol):
        self._secure = False
        self._interval = 0
        self._bootstrap = None
        self._port = 0
        self._address = None
        self._devices = None
        self._channelGroup = "DefaultChannelGroup(GlobalEventExecutor.INSTANCE)"

        self._secure = config.getBoolean(Keys.PROTOCOL_SSL.withPrefix(protocol))
        self._interval = config.getLong(Keys.PROTOCOL_INTERVAL.withPrefix(protocol))
        self._address = config.getString(Keys.PROTOCOL_ADDRESS.withPrefix(protocol))
        self._port = config.getInteger(Keys.PROTOCOL_PORT.withPrefix(protocol),443 if self._secure else 80)
        self._devices = config.getString(Keys.PROTOCOL_DEVICES.withPrefix(protocol)).split("[, ]")

        pipelineFactory = self.BasePipelineFactoryAnonymousInnerClass(self, config, protocol)

        self._bootstrap = ("Bootstrap()").group(EventLoopGroupFactory.getWorkerGroup()).channel("NioSocketChannel.class").handler(pipelineFactory)

    class BasePipelineFactoryAnonymousInnerClass(BasePipelineFactory):


        def __init__(self, outerInstance, config, protocol):
            super().__init__(outerInstance, config, protocol)
            self._outerInstance = outerInstance
            self._config = config

        def addTransportHandlers(self, pipeline):
            try:
                if TrackerClient.isSecure():
                    engine = SSLContext.getDefault().createSSLEngine()
                    engine.setUseClientMode(True)
                    pipeline.addLast("SslHandler(engine)")
            except Exception as e:
                raise Exception(e)

        def addProtocolHandlers(self, pipeline):
            try:
                self._outerInstance.addProtocolHandlers(pipeline, self._config)
            except Exception as e:
                raise Exception(e)

    def addProtocolHandlers(self, pipeline, config):
        pass

    def getDevices(self):
        return self._devices

    def getChannelGroup(self):
        return self._channelGroup

    def start(self):
        self._bootstrap.connect(self._address, self._port).syncUninterruptibly().channel().closeFuture().addListener(self.GenericFutureListenerAnonymousInnerClass(self))

    class GenericFutureListenerAnonymousInnerClass():

        def __init__(self, outerInstance):
            self._outerInstance = outerInstance

        def operationComplete(self, future):
            if TrackerClient._interval > 0:
                #                            GlobalEventExecutor.INSTANCE.schedule(() ->
                #                            {
                #                                bootstrap.connect(address, port).syncUninterruptibly().channel().closeFuture().addListener(this)
                #                            }
                #                           , interval, TimeUnit.SECONDS)
                pass

    def stop(self):
        self._channelGroup.close().awaitUninterruptibly()
