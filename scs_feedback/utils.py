from dataclasses import asdict, is_dataclass
from enum import Enum
from json import dumps, loads
from typing import Any, Iterable

from django.core.serializers.json import DjangoJSONEncoder

__all__ = ("DataClassJSONEncoder", "as_dict")


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
