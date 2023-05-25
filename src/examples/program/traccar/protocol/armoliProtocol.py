from src.examples.program.traccar.baseProtocol import BaseProtocol
from src.examples.program.traccar.characterDelimiterFrameDecoder import CharacterDelimiterFrameDecoder
from src.examples.program.traccar.pipelineBuilder import PipelineBuilder
from src.examples.program.traccar.trackerServer import TrackerServer
from src.examples.program.traccar.config.config import Config

class ArmoliProtocol(BaseProtocol):

    def __init__(self, config):
        self.addServer(self.TrackerServerAnonymousInnerClass(self, config, self.getName()))

    class TrackerServerAnonymousInnerClass(TrackerServer):

        def __init__(self, outerInstance, config, getName):
            super().__init__(config, getName, False)
            self._outerInstance = outerInstance

        def addProtocolHandlers(self, pipeline, config):
            pipeline.addLast(CharacterDelimiterFrameDecoder(1024, ";;", ";\r", ";"))
            pipeline.addLast("StringEncoder()")
            pipeline.addLast("StringDecoder()")
            pipeline.addLast(ArmoliProtocolDecoder(self._outerInstance))
            pipeline.addLast(ArmoliProtocolPoller(self._outerInstance))
