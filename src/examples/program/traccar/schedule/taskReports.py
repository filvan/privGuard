import collections
import sys
from datetime import date

from kafka.metrics.stats.rate import TimeUnit

from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.model.calendar import Calendar
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.group import Group
from src.examples.program.traccar.model.report import Report
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.reports.eventsReportProvider import EventsReportProvider
from src.examples.program.traccar.reports.routeReportProvider import RouteReportProvider
from src.examples.program.traccar.reports.stopsReportProvider import StopsReportProvider
from src.examples.program.traccar.reports.summaryReportProvider import SummaryReportProvider
from src.examples.program.traccar.reports.common.reportMailer import ReportMailer
from src.examples.program.traccar.reports.tripsReportProvider import TripsReportProvider
from src.examples.program.traccar.schedule.scheduleTask import ScheduleTask
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class TaskReports(ScheduleTask):

    _LOGGER = "LoggerFactory.getLogger(TaskReports.__class__)"

    _CHECK_PERIOD_MINUTES = 1


    def __init__(self, storage, injector):

        self._storage = None
        self._injector = None

        self._storage = storage
        self._injector = injector

    def schedule(self, executor):
        executor.scheduleAtFixedRate(self, TaskReports._CHECK_PERIOD_MINUTES, TaskReports._CHECK_PERIOD_MINUTES, TimeUnit.MINUTES)

    def run(self):
        currentCheck = date()
        lastCheck = date(sys.currentTimeMillis() - TimeUnit.MINUTES.toMillis(TaskReports._CHECK_PERIOD_MINUTES))

        try:
            for report in self._storage.getObjects(Report.__class__, Request(Columns.All())):
                calendar = self._storage.getObject(Calendar.__class__, Request(Columns.All(), Condition.Equals("id", report.getCalendarId())))

                lastEvents = calendar.findPeriods(lastCheck)
                currentEvents = calendar.findPeriods(currentCheck)

                if (not lastEvents.isEmpty()) and currentEvents.isEmpty():
                    period = lastEvents.iterator().next()
                    scope = "ServletScopes.scopeRequest(Collections.emptyMap())"
                    with scope.open() as ignored:
                        self._executeReport(report, period.getStart(), period.getEnd())
        except StorageException as e:
            TaskReports._LOGGER.warn("Scheduled reports error", e)

    def _executeReport(self, report, from_, to):

        deviceIds = self._storage.getObjects(Device.__class__, Request(Columns.Include("id"), Condition.Permission(Device.__class__, Report.__class__, report.getId()))).stream().map(BaseModel.getId()).collect(collections.toList())
        groupIds = self._storage.getObjects(Group.__class__, Request(Columns.Include("id"), Condition.Permission(Group.__class__, Report.__class__, report.getId()))).stream().map(BaseModel.getId()).collect(collections.toList())
        users = self._storage.getObjects(User.__class__, Request(Columns.Include("id"), Condition.Permission(User.__class__, Report.__class__, report.getId())))

        reportMailer = self._injector.getInstance(ReportMailer.__class__)

        for user in users:
            if report.getType() is "events":
                eventsReportProvider = self._injector.getInstance(EventsReportProvider.__class__)
                reportMailer.sendAsync(user.getId(), lambda stream : eventsReportProvider.getExcel(stream, user.getId(), deviceIds, groupIds, list(), from_, to))
            elif report.getType() is "route":
                routeReportProvider = self._injector.getInstance(RouteReportProvider.__class__)
                reportMailer.sendAsync(user.getId(), lambda stream : routeReportProvider.getExcel(stream, user.getId(), deviceIds, groupIds, from_, to))
            elif report.getType() is "summary":
                summaryReportProvider = self._injector.getInstance(SummaryReportProvider.__class__)
                reportMailer.sendAsync(user.getId(), lambda stream : summaryReportProvider.getExcel(stream, user.getId(), deviceIds, groupIds, from_, to, False))
            elif report.getType() is "trips":
                tripsReportProvider = self._injector.getInstance(TripsReportProvider.__class__)
                reportMailer.sendAsync(user.getId(), lambda stream : tripsReportProvider.getExcel(stream, user.getId(), deviceIds, groupIds, from_, to))
            elif report.getType() is "stops":
                stopsReportProvider = self._injector.getInstance(StopsReportProvider.__class__)
                reportMailer.sendAsync(user.getId(), lambda stream : stopsReportProvider.getExcel(stream, user.getId(), deviceIds, groupIds, from_, to))
            else:
                TaskReports._LOGGER.warn("Unsupported report type {}", report.getType())
