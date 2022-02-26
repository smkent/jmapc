from dataclasses import dataclass

from jmapc.serializer import Model


@dataclass
class TestModel(Model):
    camel_case_key: str


def test_serializer() -> None:
    d = TestModel(camel_case_key="fourside")
    to_dict = d.to_dict()
    assert to_dict == dict(camelCaseKey="fourside")
    from_dict = TestModel.from_dict(to_dict)
    assert from_dict == d
