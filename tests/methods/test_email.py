from datetime import datetime, timezone

import responses

from jmapc import Client, Email, EmailAddress
from jmapc.methods import EmailGet, EmailGetResponse

from ..utils import expect_jmap_call


def test_identity_get(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Email/get",
                {
                    "accountId": "u1138",
                    "ids": ["f0001", "f1000"],
                    "fetchTextBodyValues": False,
                    "fetchHTMLBodyValues": False,
                    "fetchAllBodyValues": False,
                    "maxBodyValueBytes": 42,
                },
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
                "Email/get",
                {
                    "accountId": "u1138",
                    "list": [
                        {
                            "id": "f0001",
                            "threadId": "T1",
                            "mailboxIds": {
                                "MBX1": True,
                                "MBX5": True,
                            },
                            "from": [
                                {
                                    "name": "Paula",
                                    "email": "paula@twoson.example.net",
                                }
                            ],
                            "reply_to": [
                                {
                                    "name": "Paula",
                                    "email": "paula-reply@twoson.example.net",
                                }
                            ],
                            "subject": (
                                "I'm taking a day trip to Happy Happy Village"
                            ),
                            "receivedAt": "1994-08-24T12:01:02Z",
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
        EmailGet(
            ids=["f0001", "f1000"],
            fetch_text_body_values=False,
            fetch_html_body_values=False,
            fetch_all_body_values=False,
            max_body_value_bytes=42,
        )
    ) == EmailGetResponse(
        account_id="u1138",
        state="2187",
        not_found=[],
        data=[
            Email(
                id="f0001",
                thread_id="T1",
                mailbox_ids={"MBX1": True, "MBX5": True},
                mail_from=[
                    EmailAddress(
                        name="Paula", email="paula@twoson.example.net"
                    ),
                ],
                reply_to=[
                    EmailAddress(
                        name="Paula", email="paula-reply@twoson.example.net"
                    ),
                ],
                subject="I'm taking a day trip to Happy Happy Village",
                received_at=datetime(
                    1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc
                ),
            ),
        ],
    )
