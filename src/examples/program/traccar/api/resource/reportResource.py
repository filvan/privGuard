from django.http.request import HttpHeaders
from kafka.protocol.api import Response

from src.examples.program.traccar.api.simpleObjectResource import SimpleObjectResource
from src.examples.program.traccar.helper.logAction import LogAction
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.report import Report
from src.examples.program.traccar.model.userRestriction import UserRestrictions
from src.examples.program.traccar.reports.combinedReportProvider import CombinedReportItem
from src.examples.program.traccar.reports.eventsReportProvider import EventsReportProvider
from src.examples.program.traccar.reports.routeReportProvider import RouteReportProvider
from src.examples.program.traccar.reports.stopsReportProvider import StopsReportProvider
from src.examples.program.traccar.reports.summaryReportProvider import SummaryReportProvider
from src.examples.program.traccar.reports.tripsReportProvider import TripsReportProvider
from src.examples.program.traccar.reports.common.reportExecutor import ReportExecutor
from src.examples.program.traccar.reports.common.reportMailer import ReportMailer
from src.examples.program.traccar.reports.model.combinedReportItem import CombinedReportItem
from src.examples.program.traccar.reports.model.stopReportItem import StopReportItem
from src.examples.program.traccar.reports.model.summaryReportItem import SummaryReportItem
from src.examples.program.traccar.reports.model.tripReportItem import TripReportItem
from src.examples.program.traccar.storage.storageException import StorageException

class ReportResource(SimpleObjectResource):

    _EXCEL = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"








    def __init__(self):
        self._combinedReportProvider = None
        self._eventsReportProvider = None
        self._routeReportProvider = None
        self._stopsReportProvider = None
        self._summaryReportProvider = None
        self._tripsReportProvider = None
        self._reportMailer = None

        super().__init__(Report.__class__)

    def _executeReport(self, userId, mail, executor):
        if mail:
            self._reportMailer.sendAsync(userId, executor)
            return Response.noContent().build()
        else:
            #            StreamingOutput stream = output ->
            #            {
            #                try
            #                {
            #                    executor.execute(output)
            #                }
            #                catch (StorageException e)
            #                {
            #                    throw new WebApplicationException(e)
            #                }
            #            }
            return Response.ok(self.stream).header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=report.xlsx").build()

    def getCombined(self, deviceIds, groupIds, from_, to):
        self.permissions_service.checkRestriction(self.get_user_id(), UserRestrictions.getDisableReports())
        LogAction.logReport(self.get_user_id(), "combined", from_, to, deviceIds, groupIds)
        return self._combinedReportProvider.getObjects(self.get_user_id(), deviceIds, groupIds, from_, to)

    def getRoute(self, deviceIds, groupIds, from_, to):
        self.permissions_service.checkRestriction(self.get_user_id(), UserRestrictions.getDisableReports())
        LogAction.logReport(self.get_user_id(), "route", from_, to, deviceIds, groupIds)
        return self._routeReportProvider.getObjects(self.get_user_id(), deviceIds, groupIds, from_, to)

    def getRouteExcel(self, deviceIds, groupIds, from_, to, mail):
        self.permissions_service.checkRestriction(self.get_user_id(), UserRestrictions.getDisableReports())
        #        return executeReport(getUserId(), mail, stream ->
        #        {
        #            LogAction.logReport(getUserId(), "route", @from, to, deviceIds, groupIds)
        #            routeReportProvider.getExcel(stream, getUserId(), deviceIds, groupIds, @from, to)
        #        }
        #        )

    def getRouteExcel(self, deviceIds, groupIds, from_, to, type):
        return self.getRouteExcel(deviceIds, groupIds, from_, to, type == "mail")

    def getEvents(self, deviceIds, groupIds, types, from_, to):
        self.permissions_service.checkRestriction(self.get_user_id(), UserRestrictions.getDisableReports())
        LogAction.logReport(self.get_user_id(), "events", from_, to, deviceIds, groupIds)
        return self._eventsReportProvider.getObjects(self.get_user_id(), deviceIds, groupIds, types, from_, to)

    def getEventsExcel(self, deviceIds, groupIds, types, from_, to, mail):
        self.permissions_service.checkRestriction(self.get_user_id(), UserRestrictions.getDisableReports())
        #        return executeReport(getUserId(), mail, stream ->
        #        {
        #            LogAction.logReport(getUserId(), "events", @from, to, deviceIds, groupIds)
        #            eventsReportProvider.getExcel(stream, getUserId(), deviceIds, groupIds, types, @from, to)
        #        }
        #        )

    def getEventsExcel(self, deviceIds, groupIds, types, from_, to, type):
        return self.getEventsExcel(deviceIds, groupIds, types, from_, to, type == "mail")

    def getSummary(self, deviceIds, groupIds, from_, to, daily):
        self.permissions_service.checkRestriction(self.get_user_id(), UserRestrictions.getDisableReports())
        LogAction.logReport(self.get_user_id(), "summary", from_, to, deviceIds, groupIds)
        return self._summaryReportProvider.getObjects(self.get_user_id(), deviceIds, groupIds, from_, to, daily)

    def getSummaryExcel(self, deviceIds, groupIds, from_, to, daily, mail):
        self.permissions_service.checkRestriction(self.get_user_id(), UserRestrictions.getDisableReports())
        #        return executeReport(getUserId(), mail, stream ->
        #        {
        #            LogAction.logReport(getUserId(), "summary", @from, to, deviceIds, groupIds)
        #            summaryReportProvider.getExcel(stream, getUserId(), deviceIds, groupIds, @from, to, daily)
        #        }
        #        )

#JAVA TO PYTHON CONVERTER TASK: Java annotations have no direct Python equivalent:
#ORIGINAL LINE: @Path("summary/{type:xlsx|mail}") @GET @Produces(EXCEL) public Response getSummaryExcel(@QueryParam("deviceId") List<Long> deviceIds, @QueryParam("groupId") List<Long> groupIds, @QueryParam("from") Date from, @QueryParam("to") Date to, @QueryParam("daily") boolean daily, @PathParam("type") String type) throws StorageException
#JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
#JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def getSummaryExcel(self, deviceIds, groupIds, from_, to, daily, type):
        return self.getSummaryExcel(deviceIds, groupIds, from_, to, daily, type == "mail")

    def getTrips(self, deviceIds, groupIds, from_, to):
        self.permissions_service.checkRestriction(self.get_user_id(), UserRestrictions.getDisableReports())
        LogAction.logReport(self.get_user_id(), "trips", from_, to, deviceIds, groupIds)
        return self._tripsReportProvider.getObjects(self.get_user_id(), deviceIds, groupIds, from_, to)

    def getTripsExcel(self, deviceIds, groupIds, from_, to, mail):
        self.permissions_service.checkRestriction(self.get_user_id(), UserRestrictions.getDisableReports())
        #        return executeReport(getUserId(), mail, stream ->
        #        {
        #            LogAction.logReport(getUserId(), "trips", @from, to, deviceIds, groupIds)
        #            tripsReportProvider.getExcel(stream, getUserId(), deviceIds, groupIds, @from, to)
        #        }
        #        )

    def getTripsExcel(self, deviceIds, groupIds, from_, to, type):
        return self.getTripsExcel(deviceIds, groupIds, from_, to, type == "mail")

    def getStops(self, deviceIds, groupIds, from_, to):
        self.permissions_service.checkRestriction(self.get_user_id(), UserRestrictions.getDisableReports())
        LogAction.logReport(self.get_user_id(), "stops", from_, to, deviceIds, groupIds)
        return self._stopsReportProvider.getObjects(self.get_user_id(), deviceIds, groupIds, from_, to)

    def getStopsExcel(self, deviceIds, groupIds, from_, to, mail):
        self.permissions_service.checkRestriction(self.get_user_id(), UserRestrictions.getDisableReports())
        #        return executeReport(getUserId(), mail, stream ->
        #        {
        #            LogAction.logReport(getUserId(), "stops", @from, to, deviceIds, groupIds)
        #            stopsReportProvider.getExcel(stream, getUserId(), deviceIds, groupIds, @from, to)
        #        }
        #        )

    def getStopsExcel(self, deviceIds, groupIds, from_, to, type):
        return self.getStopsExcel(deviceIds, groupIds, from_, to, type == "mail")

