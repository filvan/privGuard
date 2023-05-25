from src.examples.program.traccar.baseProtocol import BaseProtocol
from src.examples.program.traccar.baseProtocolDecoder import BaseProtocolDecoder
from src.examples.program.traccar.helper.parser import Parser
from src.examples.program.traccar.helper.patternBuilder import PatternBuilder
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.pipelineBuilder import PipelineBuilder
from src.examples.program.traccar.trackerServer import TrackerServer
from src.examples.program.traccar.config.config import Config

class AppelloProtocolDecoder(BaseProtocolDecoder):

    def __init__(self, protocol):
        super().__init__(protocol)

    _PATTERN = PatternBuilder().text("FOLLOWIT,").number("(d+),").groupBegin().number("(dd)(dd)(dd)").number("(dd)(dd)(dd).?d*,").or_().text("UTCTIME,").groupEnd().number("(-?d+.d+),").number("(-?d+.d+),").number("(d+),").number("(d+),").number("(d+),").number("(-?d+),").expression("([FL]),").any().compile()

    def decode(self, channel, remoteAddress, msg):

        parser = Parser(AppelloProtocolDecoder._PATTERN, str(msg))
        if not parser.matches():
            return None

        imei = parser.next()
        deviceSession = self.getDeviceSession(channel, remoteAddress, imei)
        if deviceSession is None:
            return None

        position = Position(self.getProtocolName())
        position.setDeviceId(deviceSession.getDeviceId())

        if parser.hasNext(6):
            position.setTime(parser.nextDateTime())
        else:
            self.getLastLocation(position, None)

        position.setLatitude(parser.nextDouble(0))
        position.setLongitude(parser.nextDouble(0))
        position.setSpeed(parser.nextDouble(0))
        position.setCourse(parser.nextDouble(0))

        position.set(Position.KEY_SATELLITES, parser.nextInt(0))

        position.setAltitude(parser.nextDouble(0))

        position.setValid(parser.next() is "F")

        return position
