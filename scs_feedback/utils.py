from dataclasses import asdict, is_dataclass
from enum import Enum
from json import dumps, loads
from typing import Any, Iterable

from django.core.serializers.json import DjangoJSONEncoder

__all__ = ("ChoicesEnum", "DataClassJSONEncoder", "as_dict")


class ChoicesEnum(Enum):
    """
    Custom Enum class, heavily inspired by choicesenum package
    https://pypi.org/project/choicesenum/
    """

    def __new__(cls, value, display=None):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._display_ = display
        return obj

    @classmethod
    def choices(cls):
        return [(x.value, x.display) for x in cls]

    @property
    def display(self):
        return self._display_ if self._display_ is not None else \
            self._name_.replace('_', ' ').capitalize()


class DictWithoutNone(dict):
    def __init__(self, seq: Iterable = None, **kwargs):
        if seq is not None:
            for k, v in seq:
                if v is not None and getattr(v, "value", True):
                    self[k] = v
        else:
            super(DictWithoutNone, self).__init__(seq, **kwargs)


class DataClassJSONEncoder(DjangoJSONEncoder):
    def default(self, o: Any) -> Any:
        if is_dataclass(o):
            return asdict(o, dict_factory=DictWithoutNone)

        if isinstance(o, Enum):
            return o.value

        return super(DataClassJSONEncoder, self).default(o)


def as_dict(o: Any):
    return loads(dumps(o, cls=DataClassJSONEncoder))
