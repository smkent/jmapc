from dataclasses import dataclass, field
from typing import Optional

from jmapc import ResultReference
from jmapc.models import ListOrRef
from jmapc.serializer import Model


def test_camel_case() -> None:
    @dataclass
    class TestModel(Model):
        camel_case_key: str

    d = TestModel(camel_case_key="fourside")
    to_dict = d.to_dict()
    assert to_dict == dict(camelCaseKey="fourside")
    from_dict = TestModel.from_dict(to_dict)
    assert from_dict == d


def test_serialize_result_reference() -> None:
    @dataclass
    class TestModel(Model):
        ids: ListOrRef

    d = TestModel(
        ids=ResultReference(
            name="Some/method",
            path="/ids",
            result_of="method0",
        ),
    )
    to_dict = d.to_dict()
    assert to_dict == {
        "#ids": {"name": "Some/method", "path": "/ids", "resultOf": "method0"}
    }


def test_serialize_add_account_id() -> None:
    @dataclass
    class TestModel(Model):
        account_id: Optional[str] = field(init=False)
        data: str

    d = TestModel(
        data="is beautiful",
    )
    to_dict = d.to_dict(account_id="u1138")
    assert to_dict == dict(accountId="u1138", data="is beautiful")
