from typing import Any, Dict, Optional, Type, TypeVar, List, Set, Dict, Callable
from dataclasses import is_dataclass, asdict

import sys

T = TypeVar("T")


def _transformer_noop(source: str) -> str:
    return source


def _to_dataclass_38(
    dataclass_type: Type[T],
    data: Any,
    key_transformer: Callable[[str], str],
) -> T:
    from typing import get_args, get_type_hints, get_origin

    dict_value: Any

    if not is_dataclass(dataclass_type) or data is None:
        return data

    assert isinstance(data, dict)

    dataclass_dict: Dict[str, Any] = dict()

    for annotation_name, annotation_type in get_type_hints(dataclass_type).items():
        try:
            dict_value = data[key_transformer(annotation_name)]
        except KeyError:
            # TODO(braynstorm):
            #   Check if the field has default value. Only "continue" if it does.
            #   The current code is safe but will raise less readable exceptions.
            continue

        origin = get_origin(annotation_type)
        if origin is set:
            value_type = get_args(annotation_type)[0]
            dataclass_dict[annotation_name] = set(
                _to_dataclass_38(value_type, v, key_transformer) for v in dict_value
            )
        elif origin is list:
            value_type = get_args(annotation_type)[0]
            dataclass_dict[annotation_name] = [
                _to_dataclass_38(value_type, v, key_transformer) for v in dict_value
            ]
        elif origin is dict:
            key_type, value_type = get_args(annotation_type)
            assert key_type == str
            dataclass_dict[annotation_name] = {
                key: _to_dataclass_38(value_type, value, key_transformer)
                for key, value in dict_value.items()
            }
        else:
            dataclass_dict[annotation_name] = _to_dataclass_38(
                annotation_type, dict_value, key_transformer
            )

    return dataclass_type(**dataclass_dict)


def _to_dataclass_37(
    dataclass_type: Type[T],
    data: Any,
    key_transformer: Callable[[str], str],
) -> T:
    dict_value: Any

    if not is_dataclass(dataclass_type) or data is None:
        return data

    assert isinstance(data, dict)

    dataclass_dict: Dict[str, Any] = dict()

    annotations = dict()
    for c in dataclass_type.mro():
        try:
            annotations.update(c.__annotations__)
        except AttributeError:
            pass

    for annotation_name, annotation_type in annotations.items():
        try:
            dict_value = data[key_transformer(annotation_name)]
        except KeyError:
            # TODO(bozho2):
            #   Check if the field has default value. Only "continue" if it does.
            #   The current code is safe but will raise less readable exceptions.
            continue

        if (
            isinstance(annotation_type, Set.__class__)
            and annotation_type.__origin__ == set
        ):
            value_type = annotation_type.__args__[0]
            dataclass_dict[annotation_name] = set(
                _to_dataclass_37(value_type, v, key_transformer) for v in dict_value
            )
        elif (
            isinstance(annotation_type, List.__class__)
            and annotation_type.__origin__ == list
        ):
            value_type = annotation_type.__args__[0]
            dataclass_dict[annotation_name] = [
                _to_dataclass_37(value_type, v, key_transformer) for v in dict_value
            ]
        elif (
            isinstance(annotation_type, Dict.__class__)
            and annotation_type.__origin__ == dict
        ):
            key_type = annotation_type.__args__[0]
            value_type = annotation_type.__args__[1]
            assert key_type == str
            dataclass_dict[annotation_name] = {
                k: _to_dataclass_37(value_type, v, key_transformer)
                for k, v in dict_value.items()
            }
        else:
            dataclass_dict[annotation_name] = _to_dataclass_37(
                annotation_type, dict_value, key_transformer
            )
    return dataclass_type(**dataclass_dict)


def to_dataclass(
    dataclass_type: Type[T],
    data: Any,
    key_transformer: Optional[Callable[[str], str]] = None,
) -> T:
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

    Args:
        dataclass_type (Type[T]): The type of the root dataclass.
        data (Any): json.loads()'d data.
        key_transformer (Callable[[str], str] | None, optional):
            Name transformer function, to convert dataclass field names to
            names of the input data. Defaults to None - no transformation.

    Returns:
        T: _description_


    """
    if key_transformer is None:
        key_transformer = _transformer_noop

    if sys.version_info.minor >= 8:
        return _to_dataclass_38(dataclass_type, data, key_transformer)
    else:
        return _to_dataclass_37(dataclass_type, data, key_transformer)


def dataclass_to_dict(dataclassObject: Any) -> Dict[str, Any]:
    """
    Convert a dataclass hierarchy to a simple dict/list hierarchy.
    """
    return asdict(dataclassObject)
