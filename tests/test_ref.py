import pytest

from jmapc import Ref, ResultReference
from jmapc.methods import Invocation, MailboxGet, MailboxQuery


def test_ref_with_no_method_calls() -> None:
    method = MailboxGet(
        ids=Ref("/ids"),
    )
    with pytest.raises(ValueError):
        method.to_dict()


@pytest.mark.parametrize(
    "invalid_ref",
    [
        Ref("/ids", method="1.does_not_exist"),
        Ref("/ids", method=-6),
    ],
)
def test_ref_with_no_method_match(invalid_ref: Ref) -> None:
    method = MailboxGet(
        ids=invalid_ref,
    )
    with pytest.raises(IndexError):
        method.to_dict(
            method_calls_slice=[
                Invocation(id="0.example", method=MailboxGet(ids=[]))
            ]
        )


def test_invalid_ref_object() -> None:
    bad_ref = Ref("/ids")
    bad_ref._ref_sentinel = "invalid_value"
    method = MailboxGet(ids=bad_ref)
    with pytest.raises(ValueError):
        method.to_dict()


def test_method_with_result_reference() -> None:
    method = MailboxGet(
        ids=ResultReference(
            name=MailboxQuery.get_method_name(),
            path="/ids",
            result_of="0",
        ),
    )
    assert method.to_dict() == {
        "#ids": {"name": "Mailbox/query", "path": "/ids", "resultOf": "0"}
    }
