from jmapc import ResultReference
from jmapc.methods import MailboxGet, MailboxQuery


def test_method_with_result_reference() -> None:
    method = MailboxGet(
        ids=ResultReference(
            name=MailboxQuery.name,
            path="/ids",
            result_of="0",
        ),
    )
    assert method.to_dict() == {
        "#ids": {"name": "Mailbox/query", "path": "/ids", "resultOf": "0"}
    }
