import os

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.helper.model.deviceUtil import DeviceUtil
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.geofence import Geofence
from src.examples.program.traccar.model.group import Group
from src.examples.program.traccar.model.maintenance import Maintenance
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.reports.common.reportUtils import ReportUtils
from src.examples.program.traccar.reports.model.deviceReportSection import DeviceReportSection
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.order import Order
from src.examples.program.traccar.storage.query.request import Request

class EventsReportProvider:


    def __init__(self, config, reportUtils, storage):

        self._config = None
        self._reportUtils = None
        self._storage = None

        self._config = config
        self._reportUtils = reportUtils
        self._storage = storage

    def _getEvents(self, deviceId, from_, to):
        return self._storage.getObjects(Event.__class__, Request(Columns.All(), Condition.And(Condition.Equals("deviceId", deviceId), Condition.Between("eventTime", "from", from_, "to", to)), Order("eventTime")))

    def getObjects(self, userId, deviceIds, groupIds, types, from_, to):
        self._reportUtils.checkPeriodLimit(from_, to)

        result = []
        for device in DeviceUtil.getAccessibleDevices(self._storage, userId, deviceIds, groupIds):
            events = self._getEvents(device.getId(), from_, to)
            all = not types or Event.ALL_EVENTS in types
            for event in events:
                if all or event.getType() in types:
                    geofenceId = event.getGeofenceId()
                    maintenanceId = event.getMaintenanceId()
                    if (geofenceId == 0 or self._reportUtils.getObject(userId, Geofence.__class__, geofenceId) is not None) and (maintenanceId == 0 or self._reportUtils.getObject(userId, Maintenance.__class__, maintenanceId) is not None):
                        result.append(event)
        return result

    def getExcel(self, outputStream, userId, deviceIds, groupIds, types, from_, to):
        self._reportUtils.checkPeriodLimit(from_, to)

        devicesEvents = []
        sheetNames = []
        geofenceNames = {}
        maintenanceNames = {}
        positions = {}
        for device in DeviceUtil.getAccessibleDevices(self._storage, userId, deviceIds, groupIds):
            events = self._getEvents(device.getId(), from_, to)
            all = not types or Event.ALL_EVENTS in types
            iterator = events.iterator()
            while iterator.hasNext():
                event = iterator.next()
                if all or event.getType() in types:
                    geofenceId = event.getGeofenceId()
                    maintenanceId = event.getMaintenanceId()
                    if geofenceId != 0:
                        geofence = self._reportUtils.getObject(userId, Geofence.__class__, geofenceId)
                        if geofence is not None:
                            geofenceNames[geofenceId] = geofence.getName()
                        else:
                            iterator.remove()
                    elif maintenanceId != 0:
                        maintenance = self._reportUtils.getObject(userId, Maintenance.__class__, maintenanceId)
                        if maintenance is not None:
                            maintenanceNames[maintenanceId] = maintenance.getName()
                        else:
                            iterator.remove()
                else:
                    iterator.remove()
            for event in events:
                positionId = event.getPositionId()
                if positionId > 0:
                    position = self._storage.getObject(Position.__class__, Request(Columns.All(), Condition.Equals("id", positionId)))
                    positions[positionId] = position
            deviceEvents = DeviceReportSection()
            deviceEvents.setDeviceName(device.getName())
            sheetNames.append("WorkbookUtil.createSafeSheetName(deviceEvents.getDeviceName())")
            if device.getGroupId() > 0:
                group = self._storage.getObject(Group.__class__, Request(Columns.All(), Condition.Equals("id", device.getGroupId())))
                if group is not None:
                    deviceEvents.setGroupName(group.getName())
            deviceEvents.setObjects(events)
            devicesEvents.append(deviceEvents)

        file = os.path.get(self._config.getString(Keys.TEMPLATES_ROOT), "export", "events.xlsx").toFile()
        with "FileInputStream(file)" as inputStream:
            context = self._reportUtils.initializeContext(userId)
            context.putVar("devices", devicesEvents)
            context.putVar("sheetNames", sheetNames)
            context.putVar("geofenceNames", geofenceNames)
            context.putVar("maintenanceNames", maintenanceNames)
            context.putVar("positions", positions)
            context.putVar("from", from_)
            context.putVar("to", to)
            self._reportUtils.processTemplateWithSheets(inputStream, outputStream, context)
