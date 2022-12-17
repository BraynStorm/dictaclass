from typing import Any, Dict, Type, TypeVar, get_args, get_type_hints, get_origin

from dataclasses import is_dataclass, asdict

T = TypeVar("T")


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
                to_dataclass(value_type, v) for v in dict_value
            )
        elif origin is list:
            value_type = get_args(annotation_type)[0]
            dataclass_dict[annotation_name] = [
                to_dataclass(value_type, v) for v in dict_value
            ]
        elif origin is dict:
            key_type, value_type = get_args(annotation_type)
            assert key_type == str
            dataclass_dict[annotation_name] = {
                key: to_dataclass(value_type, value)
                for key, value in dict_value.items()
            }
        else:
            dataclass_dict[annotation_name] = to_dataclass(annotation_type, dict_value)

    return dataclass_type(**dataclass_dict)


def dataclass_to_dict(dataclassObject: Any) -> Dict[str, Any]:
    """
    Convert a dataclass hierarchy to a simple dict/list hierarchy.
    """
    return asdict(dataclassObject)
