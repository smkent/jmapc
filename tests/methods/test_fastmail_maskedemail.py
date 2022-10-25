from datetime import datetime, timezone

import responses

from jmapc import Client
from jmapc.fastmail import (
    MaskedEmail,
    MaskedEmailGet,
    MaskedEmailGetResponse,
    MaskedEmailSet,
    MaskedEmailSetResponse,
)

from ..utils import expect_jmap_call


def test_maskedemail_get(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "MaskedEmail/get",
                {"accountId": "u1138", "ids": ["masked-1138"]},
                "single.MaskedEmail/get",
            ]
        ],
        "using": [
            "https://www.fastmail.com/dev/maskedemail",
            "urn:ietf:params:jmap:core",
        ],
    }
    response = {
        "methodResponses": [
            [
                "MaskedEmail/get",
                {
                    "accountId": "u1138",
                    "list": [
                        {
                            "id": "masked-1138",
                            "email": "pk.fire@ness.example.com",
                            "forDomain": "ness.example.com",
                            "description": (
                                "Masked Email (pk.fire@ness.example.com)"
                            ),
                            "lastMessageAt": "1994-08-24T12:01:02Z",
                            "createdAt": "1994-08-24T12:01:02Z",
                            "createdBy": "ness",
                            "url": None,
                        },
                    ],
                    "not_found": [],
                    "state": "2187",
                },
                "single.MaskedEmail/get",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    jmap_response = client.request(MaskedEmailGet(ids=["masked-1138"]))
    assert jmap_response == MaskedEmailGetResponse(
        account_id="u1138",
        state="2187",
        not_found=[],
        data=[
            MaskedEmail(
                id="masked-1138",
                email="pk.fire@ness.example.com",
                for_domain="ness.example.com",
                description="Masked Email (pk.fire@ness.example.com)",
                last_message_at=datetime(
                    1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc
                ),
                created_at=datetime(
                    1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc
                ),
                created_by="ness",
            ),
        ],
    )


def test_maskedemail_set(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "MaskedEmail/set",
                {
                    "accountId": "u1138",
                    "create": {
                        "create": {
                            "email": "pk.fire@ness.example.com",
                            "forDomain": "ness.example.com",
                            "description": (
                                "Masked Email (pk.fire@ness.example.com)"
                            ),
                            "lastMessageAt": "1994-08-24T12:01:02Z",
                            "createdAt": "1994-08-24T12:01:02Z",
                            "createdBy": "ness",
                        },
                    },
                },
                "single.MaskedEmail/set",
            ]
        ],
        "using": [
            "https://www.fastmail.com/dev/maskedemail",
            "urn:ietf:params:jmap:core",
        ],
    }
    response = {
        "methodResponses": [
            [
                "MaskedEmail/set",
                {
                    "accountId": "u1138",
                    "created": {
                        "create": {
                            "id": "masked-42",
                            "email": "pk.fire@ness.example.com",
                            "forDomain": "ness.example.com",
                            "description": (
                                "Masked Email (pk.fire@ness.example.com)"
                            ),
                            "lastMessageAt": "1994-08-24T12:01:02Z",
                            "createdAt": "1994-08-24T12:01:02Z",
                            "createdBy": "ness",
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
                "single.MaskedEmail/set",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)

    assert client.request(
        MaskedEmailSet(
            create=dict(
                create=MaskedEmail(
                    id=None,
                    email="pk.fire@ness.example.com",
                    for_domain="ness.example.com",
                    description="Masked Email (pk.fire@ness.example.com)",
                    last_message_at=datetime(
                        1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc
                    ),
                    created_at=datetime(
                        1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc
                    ),
                    created_by="ness",
                )
            )
        )
    ) == MaskedEmailSetResponse(
        account_id="u1138",
        old_state="1",
        new_state="2",
        created=dict(
            create=MaskedEmail(
                id="masked-42",
                email="pk.fire@ness.example.com",
                for_domain="ness.example.com",
                description="Masked Email (pk.fire@ness.example.com)",
                last_message_at=datetime(
                    1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc
                ),
                created_at=datetime(
                    1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc
                ),
                created_by="ness",
            ),
        ),
        updated=None,
        destroyed=None,
        not_created=None,
        not_updated=None,
        not_destroyed=None,
    )
