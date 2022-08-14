import responses

from jmapc import AddedItem, Client, Mailbox, MailboxQueryFilterCondition
from jmapc.methods import (
    MailboxChanges,
    MailboxChangesResponse,
    MailboxGet,
    MailboxGetResponse,
    MailboxQuery,
    MailboxQueryChanges,
    MailboxQueryChangesResponse,
    MailboxQueryResponse,
    MailboxSet,
    MailboxSetResponse,
)

from ..utils import expect_jmap_call


def test_mailbox_changes(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Mailbox/changes",
                {
                    "accountId": "u1138",
                    "sinceState": "2999",
                    "maxChanges": 47,
                },
                "single.Mailbox/changes",
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
                "Mailbox/changes",
                {
                    "accountId": "u1138",
                    "oldState": "2999",
                    "newState": "3000",
                    "hasMoreChanges": False,
                    "created": ["MBX0001", "MBX0002"],
                    "updated": [],
                    "destroyed": ["MBX0003"],
                },
                "single.Mailbox/changes",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
        MailboxChanges(since_state="2999", max_changes=47)
    ) == MailboxChangesResponse(
        account_id="u1138",
        old_state="2999",
        new_state="3000",
        has_more_changes=False,
        created=["MBX0001", "MBX0002"],
        updated=[],
        destroyed=["MBX0003"],
    )


def test_mailbox_get(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Mailbox/get",
                {"accountId": "u1138", "ids": ["MBX1", "MBX1000"]},
                "single.Mailbox/get",
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
                "single.Mailbox/get",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
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


def test_mailbox_query(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Mailbox/query",
                {
                    "accountId": "u1138",
                    "filter": {
                        "name": "Inbox",
                    },
                },
                "single.Mailbox/query",
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
                "Mailbox/query",
                {
                    "accountId": "u1138",
                    "ids": ["MBX1", "MBX5"],
                    "queryState": "4000",
                    "canCalculateChanges": True,
                    "position": 42,
                    "total": 9001,
                    "limit": 256,
                },
                "single.Mailbox/query",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
        MailboxQuery(filter=MailboxQueryFilterCondition(name="Inbox"))
    ) == MailboxQueryResponse(
        account_id="u1138",
        ids=["MBX1", "MBX5"],
        query_state="4000",
        can_calculate_changes=True,
        position=42,
        total=9001,
        limit=256,
    )


def test_mailbox_query_changes(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Mailbox/queryChanges",
                {
                    "accountId": "u1138",
                    "filter": {
                        "name": "Inbox",
                    },
                    "sinceQueryState": "1000",
                    "calculateTotal": False,
                },
                "single.Mailbox/queryChanges",
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
                "Mailbox/queryChanges",
                {
                    "accountId": "u1138",
                    "oldQueryState": "1000",
                    "newQueryState": "1003",
                    "added": [
                        {
                            "id": "MBX8002",
                            "index": 3,
                        },
                        {
                            "id": "MBX8003",
                            "index": 8,
                        },
                    ],
                    "removed": ["MBX8001"],
                    "total": 42,
                },
                "single.Mailbox/queryChanges",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(
        MailboxQueryChanges(
            filter=MailboxQueryFilterCondition(name="Inbox"),
            since_query_state="1000",
        )
    ) == MailboxQueryChangesResponse(
        account_id="u1138",
        old_query_state="1000",
        new_query_state="1003",
        removed=["MBX8001"],
        added=[
            AddedItem(id="MBX8002", index=3),
            AddedItem(id="MBX8003", index=8),
        ],
        total=42,
    )


def test_mailbox_set(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Mailbox/set",
                {
                    "accountId": "u1138",
                    "create": {
                        "mailbox": {
                            "name": "Saturn Valley Newsletter",
                            "isSubscribed": False,
                            "sortOrder": 0,
                        }
                    },
                    "onDestroyRemoveEmails": False,
                },
                "single.Mailbox/set",
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
                "Mailbox/set",
                {
                    "accountId": "u1138",
                    "oldState": "1",
                    "newState": "2",
                    "created": {
                        "mailbox": {
                            "showAsLabel": True,
                            "totalThreads": 0,
                            "unreadThreads": 0,
                            "isSeenShared": False,
                            "unreadEmails": 0,
                            "myRights": {
                                "maySubmit": True,
                                "maySetKeywords": True,
                                "mayAddItems": True,
                                "mayAdmin": True,
                                "mayRemoveItems": True,
                                "mayDelete": True,
                                "maySetSeen": True,
                                "mayCreateChild": True,
                                "mayRename": True,
                                "mayReadItems": True,
                            },
                            "totalEmails": 0,
                            "id": "MBX9000",
                        },
                    },
                    "updated": None,
                    "destroyed": None,
                    "notCreated": None,
                    "notDestroyed": None,
                    "notUpdated": None,
                },
                "single.Mailbox/set",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)

    assert client.request(
        MailboxSet(
            create=dict(mailbox=Mailbox(name="Saturn Valley Newsletter"))
        )
    ) == MailboxSetResponse(
        account_id="u1138",
        old_state="1",
        new_state="2",
        created=dict(
            mailbox=Mailbox(
                id="MBX9000",
                total_emails=0,
                unread_emails=0,
                total_threads=0,
                unread_threads=0,
            )
        ),
        updated=None,
        destroyed=None,
        not_created=None,
        not_updated=None,
        not_destroyed=None,
    )
