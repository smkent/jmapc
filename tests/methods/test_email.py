from datetime import datetime, timezone

import responses

from jmapc import (
    Client,
    Comparator,
    Email,
    EmailAddress,
    EmailBodyPart,
    EmailBodyValue,
    EmailHeader,
    EmailQueryFilterCondition,
)
from jmapc.methods import (
    EmailGet,
    EmailGetResponse,
    EmailQuery,
    EmailQueryResponse,
    EmailSet,
    EmailSetResponse,
)

from ..utils import expect_jmap_call


def test_email_get(
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
    assert client.method_call(
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


def test_email_set(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    draft = Email(
        mail_from=[
            EmailAddress(name="Paula", email="paula@twoson.example.net"),
        ],
        to=[
            EmailAddress(name="Ness", email="ness@onett.example.net"),
        ],
        subject="I'm taking a day trip to Happy Happy Village",
        keywords={"$draft": True},
        mailbox_ids={"MBX1": True},
        body_values=dict(body=EmailBodyValue(value="See you there!")),
        text_body=[EmailBodyPart(part_id="body", type="text/plain")],
        headers=[EmailHeader(name="X-Onett-Sanctuary", value="Giant Step")],
    )

    expected_request = {
        "methodCalls": [
            [
                "Email/set",
                {
                    "accountId": "u1138",
                    "create": {
                        "draft": {
                            "from": [
                                {
                                    "email": "paula@twoson.example.net",
                                    "name": "Paula",
                                }
                            ],
                            "to": [
                                {
                                    "email": "ness@onett.example.net",
                                    "name": "Ness",
                                }
                            ],
                            "subject": (
                                "I'm taking a day trip to "
                                "Happy Happy Village"
                            ),
                            "keywords": {"$draft": True},
                            "mailboxIds": {"MBX1": True},
                            "bodyValues": {
                                "body": {"value": "See you there!"}
                            },
                            "textBody": [
                                {"partId": "body", "type": "text/plain"}
                            ],
                            "header:X-Onett-Sanctuary": "Giant Step",
                        }
                    },
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
                "Email/set",
                {
                    "accountId": "u1138",
                    "created": {
                        "draft": {
                            "blobId": "G12345",
                            "id": "M1001",
                            "size": 42,
                            "threadId": "T1002",
                        }
                    },
                    "destroyed": None,
                    "newState": "2",
                    "notCreated": None,
                    "notDestroyed": None,
                    "notUpdated": None,
                    "oldState": "1",
                    "updated": None,
                },
                "uno",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)

    assert client.method_call(
        EmailSet(create=dict(draft=draft))
    ) == EmailSetResponse(
        account_id="u1138",
        old_state="1",
        new_state="2",
        created=dict(
            draft=Email(
                blob_id="G12345", id="M1001", size=42, thread_id="T1002"
            )
        ),
        updated=None,
        destroyed=None,
        not_created=None,
        not_updated=None,
        not_destroyed=None,
    )


def test_email_query(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Email/query",
                {
                    "accountId": "u1138",
                    "collapseThreads": True,
                    "filter": {
                        "after": "1994-08-24T12:01:02Z",
                        "inMailbox": "MBX1",
                    },
                    "limit": 10,
                    "sort": [
                        {
                            "anchorOffset": 0,
                            "calculateTotal": False,
                            "isAscending": False,
                            "position": 0,
                            "property": "receivedAt",
                        }
                    ],
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
                "Email/query",
                {
                    "accountId": "u1138",
                    "ids": ["M1000", "M1234"],
                },
                "uno",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.method_call(
        EmailQuery(
            collapse_threads=True,
            filter=EmailQueryFilterCondition(
                in_mailbox="MBX1",
                after=datetime(1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc),
            ),
            sort=[Comparator(property="receivedAt", is_ascending=False)],
            limit=10,
        )
    ) == EmailQueryResponse(
        account_id="u1138",
        ids=["M1000", "M1234"],
    )
