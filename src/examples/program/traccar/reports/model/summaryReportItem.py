from src.examples.program.traccar.reports.model.baseReportItem import BaseReportItem


class SummaryReportItem(BaseReportItem):

    def __init__(self):
        self._engineHours = 0



    def getEngineHours(self):
        return self._engineHours

    def setEngineHours(self, engineHours):
        self._engineHours = engineHours
