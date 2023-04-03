from __future__ import annotations
from typing import TypeVar, Type, List
import dacite
import datetime
import uuid

def _custom_strtime(day: str):

    try:
        return datetime.datetime.fromisoformat(day)
    except:
        pass

    return datetime.datetime.strptime(day, '%Y-%m-%dT%H:%M:%SZ')


T = TypeVar('T')

MAPPER_CONFIG = dacite.Config(
    cast = [
        uuid.UUID, 
    ],

    type_hooks = {
        datetime.datetime: _custom_strtime,
        datetime.date: datetime.date.fromisoformat,
        datetime.time: datetime.time.fromisoformat,
    },
)


def to_models(data: list[dict], class_type: Type[T]) -> List[T]:
    results = []

    for x in data:
        model = to_model(x, class_type)
        results.append(model)

    return results


def to_model(data: dict, class_type: Type[T]) -> T:
    return dacite.from_dict(class_type, data, MAPPER_CONFIG)
