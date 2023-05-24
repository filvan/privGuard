import collections
from collections.abc import Set

from src.examples.program.traccar.helper.model.deviceUtil import DeviceUtil
from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.reports.common.reportUtils import ReportUtils
from src.examples.program.traccar.reports.model.combinedReportItem import CombinedReportItem
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.order import Order
from src.examples.program.traccar.storage.query.request import Request

class CombinedReportProvider:

    _EXCLUDE_TYPES = Set.of(Event.TYPE_DEVICE_MOVING)


    def __init__(self, reportUtils, storage):

        self._reportUtils = None
        self._storage = None

        self._reportUtils = reportUtils
        self._storage = storage

    def getObjects(self, userId, deviceIds, groupIds, from_, to):
        self._reportUtils.checkPeriodLimit(from_, to)

        result = []
        for device in DeviceUtil.getAccessibleDevices(self._storage, userId, deviceIds, groupIds):
            item = CombinedReportItem()
            item.setDeviceId(device.getId())
            positions = PositionUtil.getPositions(self._storage, device.getId(), from_, to)
            item.setRoute(positions.stream().map(lambda p : [p.getLongitude(), p.getLatitude()]).collect(collections.toList()))
            events = self._storage.getObjects(Event.__class__, Request(Columns.All(), Condition.And(Condition.Equals("deviceId", device.getId()), Condition.Between("eventTime", "from", from_, "to", to)), Order("eventTime")))
            item.setEvents(events.stream().filter(lambda e : e.getPositionId() > 0 and (not CombinedReportProvider._EXCLUDE_TYPES.contains(e.getType()))).collect(collections.toList()))
            eventPositions = events.stream().map(Event.getPositionId()).collect(collections.toSet())
            item.setPositions(positions.stream().filter(lambda p : eventPositions.contains(p.getId())).collect(collections.toList()))
            result.append(item)
        return result
