from src.examples.program.traccar.baseProtocol import BaseProtocol
from src.examples.program.traccar.pipelineBuilder import PipelineBuilder
from src.examples.program.traccar.protocol.appelloProtocolDecoder import AppelloProtocolDecoder
from src.examples.program.traccar.trackerServer import TrackerServer
from src.examples.program.traccar.config.config import Config

class AppelloProtocol(BaseProtocol):

    def __init__(self, config):
        self.addServer(self.TrackerServerAnonymousInnerClass(self, config, self.getName()))

    class TrackerServerAnonymousInnerClass(TrackerServer):

        def __init__(self, outerInstance, config, getName):
            super().__init__(config, getName, False)
            self._outerInstance = outerInstance

        def addProtocolHandlers(self, pipeline, config):
            pipeline.addLast("LineBasedFrameDecoder(1024)")
            pipeline.addLast("StringDecoder()")
            pipeline.addLast("StringEncoder()")
            pipeline.addLast(AppelloProtocolDecoder(self._outerInstance))
