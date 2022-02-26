import responses

from jmapc import Client, Mailbox
from jmapc.methods import MailboxGet, MailboxGetResponse

from ..utils import expect_jmap_call


def test_identity_get(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Mailbox/get",
                {"accountId": "u1138", "ids": ["MBX1", "MBX1000"]},
                "uno",
            ]
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:mail",
        ],
    }
    response = {
        "methodResponses": [
            [
                "Mailbox/get",
                {
                    "accountId": "u1138",
                    "list": [
                        {
                            "id": "MBX1",
                            "name": "First",
                            "sortOrder": 1,
                            "totalEmails": 100,
                            "unreadEmails": 3,
                            "totalThreads": 5,
                            "unreadThreads": 1,
                            "isSubscribed": True,
                        },
                        {
                            "id": "MBX1000",
                            "name": "More Mailbox",
                            "sortOrder": 42,
                            "totalEmails": 10000,
                            "unreadEmails": 99,
                            "totalThreads": 5000,
                            "unreadThreads": 90,
                            "isSubscribed": False,
                        },
                    ],
                    "not_found": [],
                    "state": "2187",
                },
                "uno",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.call_method(
        MailboxGet(ids=["MBX1", "MBX1000"])
    ) == MailboxGetResponse(
        account_id="u1138",
        state="2187",
        not_found=[],
        data=[
            Mailbox(
                id="MBX1",
                name="First",
                sort_order=1,
                total_emails=100,
                unread_emails=3,
                total_threads=5,
                unread_threads=1,
                is_subscribed=True,
            ),
            Mailbox(
                id="MBX1000",
                name="More Mailbox",
                sort_order=42,
                total_emails=10000,
                unread_emails=99,
                total_threads=5000,
                unread_threads=90,
                is_subscribed=False,
            ),
        ],
    )
