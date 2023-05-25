from src.examples.program.traccar.baseProtocol import BaseProtocol
from src.examples.program.traccar.pipelineBuilder import PipelineBuilder
from src.examples.program.traccar.protocol.alematicsFrameDecoder import AlematicsFrameDecoder
from src.examples.program.traccar.protocol.alematicsProtocolDecoder import AlematicsProtocolDecoder
from src.examples.program.traccar.trackerServer import TrackerServer
from src.examples.program.traccar.config.config import Config

class AlematicsProtocol(BaseProtocol):

    def __init__(self, config):
        self.addServer(self.TrackerServerAnonymousInnerClass(self, config, self.getName()))

    class TrackerServerAnonymousInnerClass(TrackerServer):

        def __init__(self, outerInstance, config, getName):
            super().__init__(config, getName, False)
            self._outerInstance = outerInstance

        def addProtocolHandlers(self, pipeline, config):
            pipeline.addLast(AlematicsFrameDecoder(1024))
            pipeline.addLast("StringEncoder()")
            pipeline.addLast("StringDecoder()")
            pipeline.addLast(AlematicsProtocolDecoder(self._outerInstance))
