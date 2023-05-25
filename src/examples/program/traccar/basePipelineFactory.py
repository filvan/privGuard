from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.handler.ackowledgementHandler import AcknowledgementHandler
from src.examples.program.traccar.handler.computedAttributesHandler import ComputedAttributesHandler
from src.examples.program.traccar.handler.copyAttributesHandler import CopyAttributesHandler
from src.examples.program.traccar.handler.defaultDataHandler import DefaultDataHandler
from src.examples.program.traccar.handler.distanceHandler import DistanceHandler
from src.examples.program.traccar.handler.engineHoursHandler import EngineHoursHandler
from src.examples.program.traccar.handler.filterHandler import FilterHandler
from src.examples.program.traccar.handler.geocoderHandler import GeocoderHandler
from src.examples.program.traccar.handler.geofenceHandler import GeofenceHandler
from src.examples.program.traccar.handler.geolocationHandler import GeolocationHandler
from src.examples.program.traccar.handler.hemisphereHandler import HemisphereHandler
from src.examples.program.traccar.handler.motionHandler import MotionHandler
from src.examples.program.traccar.handler.networkForwarderHandler import NetworkForwarderHandler
from src.examples.program.traccar.handler.networkMessageHandler import NetworkMessageHandler
from src.examples.program.traccar.handler.openChannelHandler import OpenChannelHandler
from src.examples.program.traccar.handler.remoteAddressHandler import RemoteAddressHandler
from src.examples.program.traccar.handler.speedLimitHandler import SpeedLimitHandler
from src.examples.program.traccar.handler.standardLoggingHandler import StandardLoggingHandler
from src.examples.program.traccar.handler.timeHandler import TimeHandler
from src.examples.program.traccar.handler.events.alertEventHandler import AlertEventHandler
from src.examples.program.traccar.handler.events.behaviorEventHandler import BehaviorEventHandler
from src.examples.program.traccar.handler.events.commandResultEventHandler import CommandResultEventHandler
from src.examples.program.traccar.handler.events.driverEventHandler import DriverEventHandler
from src.examples.program.traccar.handler.events.fuelEventHandler import FuelEventHandler
from src.examples.program.traccar.handler.events.geofenceEventHandler import GeofenceEventHandler
from src.examples.program.traccar.handler.events.ignitionEventHandler import IgnitionEventHandler
from src.examples.program.traccar.handler.events.maintenanceEventHandler import MaintenanceEventHandler
from src.examples.program.traccar.handler.events.mediaEventHandler import MediaEventHandler
from src.examples.program.traccar.handler.events.motionEventHandler import MotionEventHandler
from src.examples.program.traccar.handler.events.overspeedEventHandler import OverspeedEventHandler
from src.examples.program.traccar.positionForwardingHandler import PositionForwardingHandler
from src.examples.program.traccar.wrapperInboundHandler import WrapperInboundHandler
from src.examples.program.traccar.wrapperOutboundHandler import WrapperOutboundHandler


class BasePipelineFactory():


    def __init__(self, connector, config, protocol):
        self._injector = None
        self._connector = None
        self._config = None
        self._protocol = None
        self._timeout = 0

        self._injector = Main.getInjector()
        self._connector = connector
        self._config = config
        self._protocol = protocol
        timeout = config.getInteger(Keys.PROTOCOL_TIMEOUT.withPrefix(protocol))
        if timeout == 0:
            self._timeout = config.getInteger(Keys.SERVER_TIMEOUT)
        else:
            self._timeout = timeout

    def addTransportHandlers(self, pipeline):
        pass

    def addProtocolHandlers(self, pipeline):
        pass

    def _addHandlers(self, pipeline, *handlerClasses):
        for handlerClass in handlerClasses:
            if handlerClass is not None:
                pipeline.addLast(self._injector.getInstance(handlerClass))

    @staticmethod
    def getHandler(pipeline, clazz):
        for handlerEntry in pipeline:
            handler = handlerEntry.getValue()
            if isinstance(handler, WrapperInboundHandler):
                handler = (handler).getWrappedHandler()
            elif isinstance(handler, WrapperOutboundHandler):
                handler = (handler).getWrappedHandler()
            if clazz.isAssignableFrom(type(handler)):
                return handler
        return None

    def initChannel(self, channel):
        pipeline = channel.pipeline()

        self.addTransportHandlers(pipeline.addLast)

        if self._timeout > 0 and not self._connector.isDatagram():
            pipeline.addLast(IdleStateHandler(self._timeout, 0, 0))
        pipeline.addLast(OpenChannelHandler(self._connector))
        if self._config.hasKey(Keys.SERVER_FORWARD):
            port = self._config.getInteger(Keys.PROTOCOL_PORT.withPrefix(self._protocol))
            handler = NetworkForwarderHandler(port)
            self._injector.injectMembers(handler)
            pipeline.addLast(handler)
        pipeline.addLast(NetworkMessageHandler())
        pipeline.addLast(StandardLoggingHandler(self._protocol))
        if not self._config.getBoolean(Keys.SERVER_INSTANT_ACKNOWLEDGEMENT):
            pipeline.addLast(AcknowledgementHandler())

        #        addProtocolHandlers(handler ->
        #        {
        #            if (handler instanceof BaseProtocolDecoder || handler instanceof BaseProtocolEncoder)
        #            {
        #                injector.injectMembers(handler)
        #            }
        #            else
        #            {
        #                if (handler instanceof ChannelInboundHandler)
        #                {
        #                    handler = new WrapperInboundHandler((ChannelInboundHandler) handler)
        #                }
        #                else
        #                {
        #                    handler = new WrapperOutboundHandler((ChannelOutboundHandler) handler)
        #                }
        #            }
        #            pipeline.addLast(handler)
        #        }
        #        )

        self._addHandlers(pipeline, TimeHandler.__class__, GeolocationHandler.__class__, HemisphereHandler.__class__, DistanceHandler.__class__, RemoteAddressHandler.__class__, FilterHandler.__class__, GeofenceHandler.__class__, GeocoderHandler.__class__, SpeedLimitHandler.__class__, MotionHandler.__class__, CopyAttributesHandler.__class__, EngineHoursHandler.__class__, ComputedAttributesHandler.__class__, PositionForwardingHandler.__class__, DefaultDataHandler.__class__, MediaEventHandler.__class__, CommandResultEventHandler.__class__, OverspeedEventHandler.__class__, BehaviorEventHandler.__class__, FuelEventHandler.__class__, MotionEventHandler.__class__, GeofenceEventHandler.__class__, AlertEventHandler.__class__, IgnitionEventHandler.__class__, MaintenanceEventHandler.__class__, DriverEventHandler.__class__, MainEventHandler.__class__)
