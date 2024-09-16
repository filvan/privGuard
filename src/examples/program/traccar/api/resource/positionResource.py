from django.http.request import HttpHeaders
from kafka.protocol.api import Response

from src.examples.program.traccar.api.baseResource import BaseResource
from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.userRestriction import UserRestrictions
from src.examples.program.traccar.reports.csvExportProvider import CsvExportProvider
from src.examples.program.traccar.reports.gpxExportProvider import GpxExportProvider
from src.examples.program.traccar.reports.kmlExportProvider import KmlExportProvider
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class PositionResource(BaseResource):

    def __init__(self):
        self._kmlExportProvider = None
        self._csvExportProvider = None
        self._gpxExportProvider = None

    def getJson(self, deviceId, positionIds, from_, to):
        if positionIds:
            positions = []
            for positionId in positionIds:
                position = self.storage.getObject(Position.__class__, Request(Columns.All(), Condition.Equals("id", positionId)))
                self.permissions_service.checkPermission(Device.__class__, self.get_user_id(), position.getDeviceId())
                positions.append(position)
            return positions
        elif deviceId > 0:
            self.permissions_service.checkPermission(Device.__class__, self.get_user_id(), deviceId)
            if from_ is not None and to is not None:
                self.permissions_service.checkRestriction(self.get_user_id(), UserRestrictions.getDisableReports())
                return PositionUtil.getPositions(self.storage, deviceId, from_, to)
            else:
                return self.storage.getObjects(Position.__class__, Request(Columns.All(), Condition.LatestPositions(deviceId)))
        else:
            return PositionUtil.getLatestPositions(self.storage, self.get_user_id())

    def remove(self, deviceId, from_, to):
        self.permissions_service.checkPermission(Device.__class__, self.get_user_id(), deviceId)
        self.permissions_service.checkRestriction(self.get_user_id(), UserRestrictions.getReadonly())

        conditions = list()
        conditions.append(Condition.Equals("deviceId", deviceId))
        conditions.append(Condition.Between("fixTime", "from", from_, "to", to))
        self.storage.removeObject(Position.__class__, Request(Condition.merge(conditions)))

        return Response.status(Response.Status.NO_CONTENT).build()

    def getKml(self, deviceId, from_, to):
        self.permissions_service.checkPermission(Device.__class__, self.get_user_id(), deviceId)
        #        StreamingOutput stream = output ->
        #        {
        #            try
        #            {
        #                kmlExportProvider.generate(output, deviceId, @from, to)
        #            }
        #            catch (StorageException e)
        #            {
        #                throw new WebApplicationException(e)
        #            }
        #        }
        return Response.ok(self.stream).header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=positions.kml").build()

    def getCsv(self, deviceId, from_, to):
        self.permissions_service.checkPermission(Device.__class__, self.get_user_id(), deviceId)
        #        StreamingOutput stream = output ->
        #        {
        #            try
        #            {
        #                csvExportProvider.generate(output, deviceId, @from, to)
        #            }
        #            catch (StorageException e)
        #            {
        #                throw new WebApplicationException(e)
        #            }
        #        }
        return Response.ok(self.stream).header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=positions.csv").build()

    def getGpx(self, deviceId, from_, to):
        self.permissions_service.checkPermission(Device.__class__, self.get_user_id(), deviceId)
        #        StreamingOutput stream = output ->
        #        {
        #            try
        #            {
        #                gpxExportProvider.generate(output, deviceId, @from, to)
        #            }
        #            catch (StorageException e)
        #            {
        #                throw new WebApplicationException(e)
        #            }
        #        }
        return Response.ok(self.stream).header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=positions.gpx").build()
