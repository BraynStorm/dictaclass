from typing import Any, Dict, Type, TypeVar, List, Set, Dict
from dataclasses import is_dataclass, asdict

import sys

T = TypeVar("T")


def _to_dataclass_38(dataclass_type: Type[T], data: Any) -> T:
    from typing import get_args, get_type_hints, get_origin

    dict_value: Any

    if not is_dataclass(dataclass_type) or data is None:
        return data

    assert isinstance(data, dict)

    dataclass_dict: Dict[str, Any] = dict()

    for annotation_name, annotation_type in get_type_hints(dataclass_type).items():
        try:
            dict_value = data[annotation_name]
        except KeyError:
            # TODO(braynstorm):
            #   Check if the field has default value. Only "continue" if it does.
            #   The current code is safe but will raise less readable exceptions.
            continue

        origin = get_origin(annotation_type)
        if origin is set:
            value_type = get_args(annotation_type)[0]
            dataclass_dict[annotation_name] = set(
                _to_dataclass_38(value_type, v) for v in dict_value
            )
        elif origin is list:
            value_type = get_args(annotation_type)[0]
            dataclass_dict[annotation_name] = [
                _to_dataclass_38(value_type, v) for v in dict_value
            ]
        elif origin is dict:
            key_type, value_type = get_args(annotation_type)
            assert key_type == str
            dataclass_dict[annotation_name] = {
                key: _to_dataclass_38(value_type, value)
                for key, value in dict_value.items()
            }
        else:
            dataclass_dict[annotation_name] = _to_dataclass_38(
                annotation_type, dict_value
            )

    return dataclass_type(**dataclass_dict)


def _to_dataclass_37(dataclass_type: Type[T], data: Any) -> T:
    dictValue: Any

    if not is_dataclass(dataclass_type) or data is None:
        return data

    assert isinstance(data, dict)

    dataclassDict: Dict[str, Any] = dict()

    for annotationName, annotationType in dataclass_type.__annotations__.items():
        try:
            dictValue = data[annotationName]
        except KeyError:
            # TODO(bozho2):
            #   Check if the field has default value. Only "continue" if it does.
            #   The current code is safe but will raise less readable exceptions.
            continue
        if (
            isinstance(annotationType, Set.__class__)
            and annotationType.__origin__ == set
        ):
            valueType = annotationType.__args__[0]
            dataclassDict[annotationName] = set(
                _to_dataclass_37(valueType, v) for v in dictValue
            )
        elif (
            isinstance(annotationType, List.__class__)
            and annotationType.__origin__ == list
        ):
            valueType = annotationType.__args__[0]
            dataclassDict[annotationName] = [
                _to_dataclass_37(valueType, v) for v in dictValue
            ]
        elif (
            isinstance(annotationType, Dict.__class__)
            and annotationType.__origin__ == dict
        ):
            keyType = annotationType.__args__[0]
            valueType = annotationType.__args__[1]
            assert keyType == str
            dataclassDict[annotationName] = {
                k: _to_dataclass_37(valueType, v) for k, v in dictValue.items()
            }
        else:
            dataclassDict[annotationName] = _to_dataclass_37(annotationType, dictValue)
    return dataclass_type(**dataclassDict)


def to_dataclass(dataclass_type: Type[T], data: Any) -> T:
    """
    Convert nested dicts/lists to a dataclass structure.

    Supported generics subtypes:
        - `List`
        - `Set`
        - `Dict`

    >>> from dataclasses import dataclass
    >>> from to_dataclass import to_dataclass
    >>> #
    >>> @dataclass
    >>> class Point
    >>>     x: int
    >>>     y: int
    >>> @dataclass
    >>> class Shape
    >>>     points: List[Point]
    >>> #
    >>> assert to_dataclass(
    >>>     Point,
    >>>     dict(
    >>>         points=[
    >>>             dict(x=0, y=0),
    >>>             dict(x=10, y=40),
    >>>         ]
    >>>     )
    >>> ) == Line(Point(0, 0), Point(10, 40))
    """

    if sys.version_info.minor >= 8:
        return _to_dataclass_38(dataclass_type, data)
    else:
        return _to_dataclass_37(dataclass_type, data)


def dataclass_to_dict(dataclassObject: Any) -> Dict[str, Any]:
    """
    Convert a dataclass hierarchy to a simple dict/list hierarchy.
    """
    return asdict(dataclassObject)
