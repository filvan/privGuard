from src.examples.program.traccar.baseProtocol import BaseProtocol
from src.examples.program.traccar.pipelineBuilder import PipelineBuilder
from src.examples.program.traccar.protocol.anytrekProtocolDecoder import AnytrekProtocolDecoder
from src.examples.program.traccar.trackerServer import TrackerServer
from src.examples.program.traccar.config.config import Config

class AnytrekProtocol(BaseProtocol):

    def __init__(self, config):
        self.addServer(self.TrackerServerAnonymousInnerClass(self, config, self.getName()))

    class TrackerServerAnonymousInnerClass(TrackerServer):

        def __init__(self, outerInstance, config, getName):
            super().__init__(config, getName, False)
            self._outerInstance = outerInstance

        def addProtocolHandlers(self, pipeline, config):
            pipeline.addLast("LengthFieldBasedFrameDecoder(ByteOrder.LITTLE_ENDIAN, 1024, 2, 2, 2, 0, True)")
            pipeline.addLast(AnytrekProtocolDecoder(self._outerInstance))
