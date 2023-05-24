import os

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.helper.model.deviceUtil import DeviceUtil
from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.group import Group
from src.examples.program.traccar.reports.common.reportUtils import ReportUtils
from src.examples.program.traccar.reports.model.deviceReportSection import DeviceReportSection
from src.examples.program.traccar.reports.model.stopReportItem import StopReportItem
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class StopsReportProvider:


    def __init__(self, config, reportUtils, storage):

        self._config = None
        self._reportUtils = None
        self._storage = None

        self._config = config
        self._reportUtils = reportUtils
        self._storage = storage

    def _detectStops(self, device, from_, to):
        ignoreOdometer = self._config.getBoolean(Keys.REPORT_IGNORE_ODOMETER)
        positions = PositionUtil.getPositions(self._storage, device.getId(), from_, to)
        return self._reportUtils.detectTripsAndStops(device, positions, ignoreOdometer, StopReportItem.__class__)

    def getObjects(self, userId, deviceIds, groupIds, from_, to):
        self._reportUtils.checkPeriodLimit(from_, to)

        result = []
        for device in DeviceUtil.getAccessibleDevices(self._storage, userId, deviceIds, groupIds):
            result.extend(self._detectStops(device, from_, to))
        return result

    def getExcel(self, outputStream, userId, deviceIds, groupIds, from_, to):
        self._reportUtils.checkPeriodLimit(from_, to)

        devicesStops = []
        sheetNames = []
        for device in DeviceUtil.getAccessibleDevices(self._storage, userId, deviceIds, groupIds):
            stops = self._detectStops(device, from_, to)
            deviceStops = DeviceReportSection()
            deviceStops.setDeviceName(device.getName())
            sheetNames.append("WorkbookUtil.createSafeSheetName(deviceStops.getDeviceName())")
            if device.getGroupId() > 0:
                group = self._storage.getObject(Group.__class__, Request(Columns.All(), Condition.Equals("id", device.getGroupId())))
                if group is not None:
                    deviceStops.setGroupName(group.getName())
            deviceStops.setObjects(stops)
            devicesStops.append(deviceStops)

        file = os.path.get(self._config.getString(Keys.TEMPLATES_ROOT), "export", "stops.xlsx").toFile()
        with "FileInputStream(file)" as inputStream:
            context = self._reportUtils.initializeContext(userId)
            context.putVar("devices", devicesStops)
            context.putVar("sheetNames", sheetNames)
            context.putVar("from", from_)
            context.putVar("to", to)
            self._reportUtils.processTemplateWithSheets(inputStream, outputStream, context)
