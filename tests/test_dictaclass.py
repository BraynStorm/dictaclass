from dictaclass.dictaclass import to_dataclass

from dataclasses import dataclass

from typing import Any, Dict, List, Set, Tuple, Type


class Test_Dictaclass:
    def test_flat(self):
        @dataclass(frozen=True)
        class ExampleDC:
            a: str
            b: int
            c: float

        v = to_dataclass(ExampleDC, dict(a="asdf", b=10, c=3.1415))

        assert isinstance(v, ExampleDC)
        assert v.a == "asdf"
        assert v.b == 10
        assert v.c == 3.1415

    def test_inheritance(self):
        @dataclass(frozen=True)
        class Base:
            a: str

        @dataclass(frozen=True)
        class Example(Base):
            b: int
            c: float

        v = to_dataclass(Example, dict(a="asdf", b=10, c=3.1415))

        assert isinstance(v, Example)
        assert v.a == "asdf"
        assert v.b == 10
        assert v.c == 3.1415

    def test_optional_values(self):
        @dataclass(frozen=True)
        class Example:
            b: int
            c: float = 0.0

        v = to_dataclass(Example, dict(b=10, c=3.1415))
        assert isinstance(v, Example)
        assert v.b == 10
        assert v.c == 3.1415

        v = to_dataclass(Example, dict(b=10))
        assert isinstance(v, Example)
        assert v.b == 10
        assert v.c == 0

    def test_with_primitive_list(self):
        @dataclass(frozen=True)
        class ExampleDC:
            a: str
            b: List[int]

        v = to_dataclass(ExampleDC, dict(a="asdf", b=[1, 2, 3]))

        assert isinstance(v, ExampleDC)
        assert v.a == "asdf"
        assert isinstance(v.b, list)
        assert v.b == [1, 2, 3]

    def test_with_primitive_set(self):
        @dataclass(frozen=True)
        class ExampleDC:
            a: str
            b: Set[int]

        v = to_dataclass(ExampleDC, dict(a="asdf", b=[1, 2, 3]))

        assert isinstance(v, ExampleDC)
        assert v.a == "asdf"
        assert isinstance(v.b, set)
        assert v.b == {1, 2, 3}

    def test_with_primitive_dict(self):
        @dataclass(frozen=True)
        class ExampleDC:
            a: str
            b: Dict[str, int]

        v = to_dataclass(ExampleDC, dict(a="asdf", b=dict(a=1, b=2)))

        assert isinstance(v, ExampleDC)
        assert v.a == "asdf"
        assert isinstance(v.b, dict)
        assert v.b == dict(a=1, b=2)

    def test_with_nested_list(self):
        @dataclass(frozen=True)
        class Pair:
            first: str
            last: str

        @dataclass(frozen=True)
        class Object:
            pairs: List[Pair]

        v = to_dataclass(
            Object,
            {
                "pairs": [
                    {"first": "f0", "last": "l0"},
                    {"first": "f1", "last": "l1"},
                ]
            },
        )
        assert isinstance(v, Object)
        assert isinstance(v.pairs, list)
        assert len(v.pairs) == 2

        assert isinstance(v.pairs[0], Pair)
        assert isinstance(v.pairs[1], Pair)

        assert isinstance(v.pairs[0].first, str)
        assert isinstance(v.pairs[0].last, str)

        assert isinstance(v.pairs[1].first, str)
        assert isinstance(v.pairs[1].last, str)

        assert v.pairs[0].first == "f0"
        assert v.pairs[0].last == "l0"
        assert v.pairs[1].first == "f1"
        assert v.pairs[1].last == "l1"

    def test_with_nested_primitive_list(self):
        @dataclass(frozen=True)
        class Object:
            pairs: List[List[str]]

        v = to_dataclass(
            Object,
            {
                "pairs": [
                    ["a", "b", "c"],
                    ["d", "e", "f"],
                ]
            },
        )
        assert isinstance(v, Object)
        assert isinstance(v.pairs, list)
        assert len(v.pairs) == 2
        assert isinstance(v.pairs[0], list)
        assert isinstance(v.pairs[1], list)
        assert v.pairs == [
            ["a", "b", "c"],
            ["d", "e", "f"],
        ]

    def test_with_nested_set(self):
        @dataclass(frozen=True)
        class Pair:
            first: str
            last: str

        @dataclass(frozen=True)
        class Object:
            pairs: Set[Pair]

        v = to_dataclass(
            Object,
            {
                "pairs": [
                    {"first": "f0", "last": "l0"},
                    {"first": "f1", "last": "l1"},
                ]
            },
        )
        assert isinstance(v, Object)
        assert isinstance(v.pairs, set)
        assert v.pairs == {
            Pair("f0", "l0"),
            Pair("f1", "l1"),
        }

    def test_with_nested_dict(self):
        @dataclass(frozen=True)
        class Pair:
            first: str
            last: str

        @dataclass(frozen=True)
        class Object:
            pairs: Dict[str, Pair]

        v = to_dataclass(
            Object,
            {
                "pairs": {
                    "p0": {"first": "f0", "last": "l0"},
                    "p1": {"first": "f1", "last": "l1"},
                }
            },
        )
        assert isinstance(v, Object)
        assert isinstance(v.pairs, dict)
        assert set(v.pairs.keys()) == {"p0", "p1"}

        assert isinstance(v.pairs["p0"], Pair)
        assert isinstance(v.pairs["p1"], Pair)

        assert isinstance(v.pairs["p0"].first, str)
        assert isinstance(v.pairs["p0"].last, str)

        assert isinstance(v.pairs["p1"].first, str)
        assert isinstance(v.pairs["p1"].last, str)

        assert v.pairs["p0"].first == "f0"
        assert v.pairs["p0"].last == "l0"
        assert v.pairs["p1"].first == "f1"
        assert v.pairs["p1"].last == "l1"

    def test_with_nested_set_2(self):
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
        assert isinstance(v.pairs, set)
        assert len(v.pairs) == 2
        assert v.pairs == {PairPair(Pair("f0", "l0")), PairPair(Pair("f1", "l1"))}

    def test_flat_with_extra_fields(self):
        @dataclass(frozen=True)
        class Pair:
            first: str
            last: str

        extras = []
        v = to_dataclass(
            Pair,
            {"first": "a", "last": "b", "middle": "lol"},
            on_extra_field=lambda klass, field_name, field_value: extras.append(
                (klass, field_name, field_value)
            ),
        )
        assert isinstance(v, Pair)
        assert v.first == "a"
        assert v.last == "b"
        assert not hasattr(v, "middle")
        assert extras == [
            (Pair, "middle", "lol"),
        ]

    def test_nested_with_extra_fields(self):
        @dataclass(frozen=True)
        class C:
            num: int

        @dataclass(frozen=True)
        class B:
            c: C

        @dataclass(frozen=True)
        class A:
            b: B

        extras: List[Tuple[Type[Any], str, Any]] = []

        def on_extra_field(*args):
            extras.append(args)

        a = to_dataclass(
            A,
            dict(b=dict(c=dict(num=10, extra_num=11), extra_num=12), extra_num=13),
            on_extra_field=on_extra_field,
        )
        assert isinstance(a, A)
        assert isinstance(a.b, B)
        assert isinstance(a.b.c, C)
        assert not hasattr(a, "extra_num")
        assert not hasattr(a.b, "extra_num")
        assert not hasattr(a.b.c, "extra_num")
        assert len(extras) == 3
        assert extras == [
            (C, "extra_num", 11),
            (B, "extra_num", 12),
            (A, "extra_num", 13),
        ]


class Test_Dictaclass_NameTransform:
    def test_to_snake_case_flat(self):
        import inflection

        @dataclass(frozen=True)
        class ExampleDC:
            url_encoded: str

        v = to_dataclass(ExampleDC, dict(UrlEncoded="asdf"), inflection.camelize)

        assert isinstance(v, ExampleDC)
        assert v.url_encoded == "asdf"
