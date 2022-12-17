# dictaclass - dicts to dataclasses

Have you ever been handed an "example JSON" and wanted to have it in an intellisense-friendly structure?
Just define the JSON structure as a hierarchy of dataclasses and run `to_dataclass(MyJsonDatatclass, json.loads(source))`


Well, the library works with whatever source of data you have, as long as you can represent the way `json.loads` does - `dict`s, `list`s, and values.


## Features

- Supports deeply nested dataclasses (duh)
- Supports inheritance
- Supports collections
  - `list`
  - `set`
  - `dict`
- Supports `frozen` dataclasses

## Limitations

- Requires Python 3.7+ 
- Cannot guess types.
- Cannot use mixed types.
- Cannot use Union[].
- Cannot use Tuple[].


## Installation

`py -m pip install dictaclass`

or

`python3 -m pip install dictaclass`

## Example

```python
from typing import Set

from dataclasses import dataclass
from dictaclass import to_dataclass

import json

@dataclass(frozen=True)
class Pair:
    first: str
    last: str

@dataclass(frozen=True)
class PairPair:
    a: Pair

@dataclass(frozen=True)
class Object:
    pairs: Set[PairPair]

v = to_dataclass(
    Object,
    {
        "pairs": [
            {"a": {"first": "f0", "last": "l0"}},
            {"a": {"first": "f1", "last": "l1"}},
        ]
    },
)
# or
v = to_dataclass(
    Object,
    json.loads(
        """
        {
            "pairs": [
                {"a": {"first": "f0", "last": "l0"}},
                {"a": {"first": "f1", "last": "l1"}}
            ]
        }
        """
    ),
)

assert isinstance(v, Object)
assert isinstance(v.pairs, set) # it was a list in the JSON
assert len(v.pairs) == 2
assert v.pairs == {
    PairPair(Pair("f0", "l0")),
    PairPair(Pair("f1", "l1"))
}
```