import responses

from jmapc import Client, Thread
from jmapc.methods import (
    ThreadChanges,
    ThreadChangesResponse,
    ThreadGet,
    ThreadGetResponse,
)

from ..utils import expect_jmap_call


def test_thread_changes(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Thread/changes",
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
                "Thread/changes",
                {
                    "accountId": "u1138",
                    "oldState": "2999",
                    "newState": "3000",
                    "hasMoreChanges": False,
                    "created": ["T0001", "T0002"],
                    "updated": [],
                    "destroyed": ["T0003"],
                },
                "uno",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.method_call(
        ThreadChanges(since_state="2999", max_changes=47)
    ) == ThreadChangesResponse(
        account_id="u1138",
        old_state="2999",
        new_state="3000",
        has_more_changes=False,
        created=["T0001", "T0002"],
        updated=[],
        destroyed=["T0003"],
    )


def test_thread_get(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Thread/get",
                {"accountId": "u1138", "ids": ["T1", "T1000"]},
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
                "Thread/get",
                {
                    "accountId": "u1138",
                    "list": [
                        {
                            "id": "T1",
                            "emailIds": [
                                "M1234",
                                "M2345",
                                "M3456",
                            ],
                        },
                        {
                            "id": "T1000",
                            "emailIds": [
                                "M1001",
                            ],
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
        ThreadGet(ids=["T1", "T1000"])
    ) == ThreadGetResponse(
        account_id="u1138",
        state="2187",
        not_found=[],
        data=[
            Thread(
                id="T1",
                email_ids=["M1234", "M2345", "M3456"],
            ),
            Thread(
                id="T1000",
                email_ids=["M1001"],
            ),
        ],
    )
