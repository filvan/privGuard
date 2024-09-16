from src.examples.program.traccar.model.groupModel import GroupedModel
from abc import ABC
from typing import List, Any


class Condition(ABC):
    @staticmethod
    def merge(conditions: List['Condition']) -> 'Condition':
        result = None
        iterator = iter(conditions)
        try:
            result = next(iterator)
            for condition in iterator:
                result = And(result, condition)
        except StopIteration:
            pass
        return result


class Compare(Condition):
    def __init__(self, column: str, operator: str, variable: str, value: Any):
        self.column = column
        self.operator = operator
        self.variable = variable
        self.value = value

    def get_column(self) -> str:
        return self.column

    def get_operator(self) -> str:
        return self.operator

    def get_variable(self) -> str:
        return self.variable

    def get_value(self) -> Any:
        return self.value


class Equals(Compare):
    def __init__(self, column: str, value: Any):
        super().__init__(column, "=", column, value)


class Between(Condition):
    def __init__(self, column: str, from_variable: str, from_value: Any, to_variable: str, to_value: Any):
        self.column = column
        self.from_variable = from_variable
        self.from_value = from_value
        self.to_variable = to_variable
        self.to_value = to_value

    def get_column(self) -> str:
        return self.column

    def get_from_variable(self) -> str:
        return self.from_variable

    def get_from_value(self) -> Any:
        return self.from_value

    def get_to_variable(self) -> str:
        return self.to_variable

    def get_to_value(self) -> Any:
        return self.to_value


class Binary(Condition):
    def __init__(self, first: Condition, second: Condition, operator: str):
        self.first = first
        self.second = second
        self.operator = operator

    def get_first(self) -> Condition:
        return self.first

    def get_second(self) -> Condition:
        return self.second

    def get_operator(self) -> str:
        return self.operator


class Or(Binary):
    def __init__(self, first: Condition, second: Condition):
        super().__init__(first, second, "OR")


class And(Binary):
    def __init__(self, first: Condition, second: Condition):
        super().__init__(first, second, "AND")


class Permission(Condition):
    def __init__(self, owner_class: type, owner_id: int, property_class: type, property_id: int = 0,
                 exclude_groups: bool = False):
        self.owner_class = owner_class
        self.owner_id = owner_id
        self.property_class = property_class
        self.property_id = property_id
        self.exclude_groups = exclude_groups

    def do_exclude_groups(self) -> 'Permission':
        return Permission(self.owner_class, self.owner_id, self.property_class, self.property_id, True)

    def get_owner_class(self) -> type:
        return self.owner_class

    def get_owner_id(self) -> int:
        return self.owner_id

    def get_property_class(self) -> type:
        return self.property_class

    def get_property_id(self) -> int:
        return self.property_id

    def get_include_groups(self) -> bool:
        owner_group_model = issubclass(self.owner_class, GroupedModel)
        property_group_model = issubclass(self.property_class, GroupedModel)
        return (owner_group_model or property_group_model) and not self.exclude_groups


class LatestPositions(Condition):
    def __init__(self, device_id: int = 0):
        self.device_id = device_id

    def get_device_id(self) -> int:
        return self.device_id
