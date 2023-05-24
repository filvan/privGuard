from src.examples.program.traccar.helper.model.userUtil import UserUtil
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.geofence import Geofence
from src.examples.program.traccar.model.maintenance import Maintenance
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.server import Server
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class NotificationFormatter:




    def __init__(self, cacheManager, textTemplateFormatter):

        self._cacheManager = None
        self._textTemplateFormatter = None

        self._cacheManager = cacheManager
        self._textTemplateFormatter = textTemplateFormatter

    def formatMessage(self, user, event, position, templatePath):

        server = self._cacheManager.getServer()
        device = self._cacheManager.getObject(Device.__class__, event.getDeviceId())

        velocityContext = self._textTemplateFormatter.prepareContext(server, user)

        velocityContext.put("device", device)
        velocityContext.put("event", event)
        if position is not None:
            velocityContext.put("position", position)
            velocityContext.put("speedUnit", UserUtil.getSpeedUnit(server, user))
            velocityContext.put("distanceUnit", UserUtil.getDistanceUnit(server, user))
            velocityContext.put("volumeUnit", UserUtil.getVolumeUnit(server, user))
        if event.getGeofenceId() != 0:
            velocityContext.put("geofence", self._cacheManager.getObject(Geofence.__class__, event.getGeofenceId()))
        if event.getMaintenanceId() != 0:
            velocityContext.put("maintenance", self._cacheManager.getObject(Maintenance.__class__, event.getMaintenanceId()))
        driverUniqueId = event.getString(Position.KEY_DRIVER_UNIQUE_ID)
        if driverUniqueId is not None:
            velocityContext.put("driver", self._cacheManager.findDriverByUniqueId(device.getId(), driverUniqueId))

        return self._textTemplateFormatter.formatMessage(velocityContext, event.getType(), templatePath)
