
from src.examples.program.traccar.helper.dateUtil import DateUtil

class DateParameterConverterProvider():

    class DateParameterConverter():

        def fromString(self, value):
            return DateUtil.parseDate(value) if value is not None else None

        def toString(self, value):
            return DateUtil.formatDate(value) if value is not None else None
