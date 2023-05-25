from src.examples.program.traccar.baseProtocol import BaseProtocol
from src.examples.program.traccar.characterDelimiterFrameDecoder import CharacterDelimiterFrameDecoder
from src.examples.program.traccar.pipelineBuilder import PipelineBuilder
from src.examples.program.traccar.protocol.arknavProtocolDecoder import ArknavProtocolDecoder
from src.examples.program.traccar.trackerServer import TrackerServer
from src.examples.program.traccar.config.config import Config

class ArknavProtocol(BaseProtocol):

    def __init__(self, config):
        self.addServer(self.TrackerServerAnonymousInnerClass(self, config, self.getName()))
        self.addServer(self.TrackerServerAnonymousInnerClass2(self, config, self.getName()))


    class TrackerServerAnonymousInnerClass(TrackerServer):

        def __init__(self, outerInstance, config, getName):
            super().__init__(config, getName, False)
            self._outerInstance = outerInstance

        def addProtocolHandlers(self, pipeline, config):
            pipeline.addLast(CharacterDelimiterFrameDecoder(1024, '\r'))
            pipeline.addLast("StringDecoder()")
            pipeline.addLast("StringEncoder()")
            pipeline.addLast(ArknavProtocolDecoder(self._outerInstance))

    class TrackerServerAnonymousInnerClass2(TrackerServer):

        def __init__(self, outerInstance, config, getName):
            super().__init__(config, getName, True)
            self._outerInstance = outerInstance

        def addProtocolHandlers(self, pipeline, config):
            pipeline.addLast("StringDecoder()")
            pipeline.addLast("StringEncoder()")
            pipeline.addLast(ArknavProtocolDecoder(self._outerInstance))
