from datetime import datetime, timezone

import responses

from jmapc import (
    AddedItem,
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
    EmailChanges,
    EmailChangesResponse,
    EmailCopy,
    EmailCopyResponse,
    EmailGet,
    EmailGetResponse,
    EmailQuery,
    EmailQueryChanges,
    EmailQueryChangesResponse,
    EmailQueryResponse,
    EmailSet,
    EmailSetResponse,
)

from ..utils import expect_jmap_call


def test_email_changes(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Email/changes",
                {
                    "accountId": "u1138",
                    "sinceState": "2999",
                    "maxChanges": 47,
                },
                "single.Email/changes",
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
                "Email/changes",
                {
                    "accountId": "u1138",
                    "oldState": "2999",
                    "newState": "3000",
                    "hasMoreChanges": False,
                    "created": ["f0001", "f0002"],
                    "updated": [],
                    "destroyed": ["f0003"],
                },
                "single.Email/changes",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
        EmailChanges(since_state="2999", max_changes=47)
    ) == EmailChangesResponse(
        account_id="u1138",
        old_state="2999",
        new_state="3000",
        has_more_changes=False,
        created=["f0001", "f0002"],
        updated=[],
        destroyed=["f0003"],
    )


def test_email_copy(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Email/copy",
                {
                    "fromAccountId": "u2187",
                    "ifFromInState": "1000",
                    "ifInState": "2000",
                    "accountId": "u1138",
                    "create": {
                        "M1001": {
                            "id": "M1001",
                        }
                    },
                    "onSuccessDestroyOriginal": False,
                    "destroyFromIfInState": "1001",
                },
                "single.Email/copy",
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
                "Email/copy",
                {
                    "fromAccountId": "u2187",
                    "accountId": "u1138",
                    "created": {
                        "M1002": {
                            "id": "M1002",
                        }
                    },
                    "oldState": "1",
                    "newState": "2",
                    "notCreated": None,
                },
                "single.Email/copy",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
        EmailCopy(
            from_account_id="u2187",
            if_from_in_state="1000",
            if_in_state="2000",
            create={"M1001": Email(id="M1001")},
            destroy_from_if_in_state="1001",
        )
    ) == EmailCopyResponse(
        account_id="u1138",
        from_account_id="u2187",
        old_state="1",
        new_state="2",
        created={"M1002": Email(id="M1002")},
        not_created=None,
    )


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
                "single.Email/get",
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
                "single.Email/get",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
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
                "single.Email/query",
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
                    "queryState": "5000",
                    "canCalculateChanges": True,
                    "position": 42,
                    "total": 9001,
                    "limit": 256,
                },
                "single.Email/query",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
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
        query_state="5000",
        can_calculate_changes=True,
        position=42,
        total=9001,
        limit=256,
    )


def test_email_query_changes(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Email/queryChanges",
                {
                    "accountId": "u1138",
                    "filter": {
                        "inMailbox": "MBX1",
                        "after": "1994-08-24T12:01:02Z",
                    },
                    "sort": [
                        {
                            "anchorOffset": 0,
                            "calculateTotal": False,
                            "isAscending": False,
                            "position": 0,
                            "property": "receivedAt",
                        }
                    ],
                    "sinceQueryState": "1000",
                    "calculateTotal": False,
                },
                "single.Email/queryChanges",
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
                "Email/queryChanges",
                {
                    "accountId": "u1138",
                    "oldQueryState": "1000",
                    "newQueryState": "1003",
                    "added": [
                        {
                            "id": "M8002",
                            "index": 3,
                        },
                        {
                            "id": "M8003",
                            "index": 8,
                        },
                    ],
                    "removed": ["M8001"],
                    "total": 42,
                },
                "single.Email/queryChanges",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
        EmailQueryChanges(
            filter=EmailQueryFilterCondition(
                in_mailbox="MBX1",
                after=datetime(1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc),
            ),
            sort=[Comparator(property="receivedAt", is_ascending=False)],
            since_query_state="1000",
        )
    ) == EmailQueryChangesResponse(
        account_id="u1138",
        old_query_state="1000",
        new_query_state="1003",
        removed=["M8001"],
        added=[
            AddedItem(id="M8002", index=3),
            AddedItem(id="M8003", index=8),
        ],
        total=42,
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
                "single.Email/set",
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
                "single.Email/set",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)

    assert client.request(
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
