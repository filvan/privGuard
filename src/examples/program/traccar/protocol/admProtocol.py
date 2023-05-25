from google.protobuf.internal.encoder import StringEncoder

from src.examples.program.traccar.baseProtocol import BaseProtocol
from src.examples.program.traccar.model.command import Command
from src.examples.program.traccar.pipelineBuilder import PipelineBuilder
from src.examples.program.traccar.protocol.admFrameDecoder import AdmFrameDecoder

from src.examples.program.traccar.protocol.admProtocolDecoder import AdmProtocolDecoder

from src.examples.program.traccar.protocol.admProtocolEncoder import AdmProtocolEncoder
from src.examples.program.traccar.trackerServer import TrackerServer
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys

class AdmProtocol(BaseProtocol):

    def __init__(self, config):
        self.setSupportedDataCommands(Command.TYPE_GET_DEVICE_STATUS, Command.TYPE_CUSTOM)
        self.addServer(self.TrackerServerAnonymousInnerClass(self, config, self.getName()))

    class TrackerServerAnonymousInnerClass(TrackerServer):

        def __init__(self, outerInstance, config, getName):
            super().__init__(config, getName, False)
            self._outerInstance = outerInstance

        def addProtocolHandlers(self, pipeline, config):
            pipeline.addLast(AdmFrameDecoder())
            pipeline.addLast(StringEncoder())
            pipeline.addLast(AdmProtocolEncoder(self._outerInstance))
            pipeline.addLast(AdmProtocolDecoder(self._outerInstance))
