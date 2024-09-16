from datetime import datetime
from typing import Type, Any, List

from src.examples.program.traccar.helper.dateUtil import DateUtil


class ParamConverter:
    def from_string(self, value: str) -> Any:
        pass

    def to_string(self, value: Any) -> str:
        pass


class DateParameterConverter(ParamConverter):
    def from_string(self, value: str) -> datetime:
        return DateUtil.parse_date(value) if value is not None else None

    def to_string(self, value: datetime) -> str:
        return DateUtil.format_date(value) if value is not None else None


class DateParameterConverterProvider:
    def get_converter(self, raw_type: Type, generic_type: Type, annotations: List[Any]):
        if raw_type == datetime:
            return DateParameterConverter()
        return None
