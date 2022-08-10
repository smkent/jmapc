import responses

from jmapc import Client, Mailbox, MailboxQueryFilterCondition
from jmapc.methods import (
    MailboxChanges,
    MailboxChangesResponse,
    MailboxGet,
    MailboxGetResponse,
    MailboxQuery,
    MailboxQueryResponse,
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
                "uno",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.method_call(
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
    assert client.method_call(
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
                "Mailbox/query",
                {
                    "accountId": "u1138",
                    "ids": ["MBX1", "MBX5"],
                },
                "uno",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.method_call(
        MailboxQuery(filter=MailboxQueryFilterCondition(name="Inbox"))
    ) == MailboxQueryResponse(
        account_id="u1138",
        ids=["MBX1", "MBX5"],
    )
