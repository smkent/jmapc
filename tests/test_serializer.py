from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import pytest
from dataclasses_json import config

from jmapc import ResultReference
from jmapc.models import ListOrRef
from jmapc.serializer import Model, datetime_decode, datetime_encode


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


@pytest.mark.parametrize(
    ["dt", "expected_dict"],
    [
        (
            datetime(2022, 2, 26, 12, 31, 45, tzinfo=timezone.utc),
            dict(timestamp="2022-02-26T12:31:45Z"),
        ),
        (None, dict()),
    ],
)
def test_serialize_datetime(
    dt: datetime, expected_dict: Dict[str, Any]
) -> None:
    @dataclass
    class TestModel(Model):
        timestamp: Optional[datetime] = field(
            default=None,
            metadata=config(encoder=datetime_encode, decoder=datetime_decode),
        )

    d = TestModel(timestamp=dt)
    to_dict = d.to_dict()
    assert to_dict == expected_dict
    from_dict = TestModel.from_dict(to_dict)
    assert from_dict == d
