import responses

from jmapc import Client, Identity
from jmapc.methods import (
    IdentityChanges,
    IdentityChangesResponse,
    IdentityGet,
    IdentityGetResponse,
    IdentitySet,
    IdentitySetResponse,
)

from ..utils import expect_jmap_call


def test_identity_changes(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Identity/changes",
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
            "urn:ietf:params:jmap:submission",
        ],
    }
    response = {
        "methodResponses": [
            [
                "Identity/changes",
                {
                    "accountId": "u1138",
                    "oldState": "2999",
                    "newState": "3000",
                    "hasMoreChanges": False,
                    "created": ["0001", "0002"],
                    "updated": [],
                    "destroyed": ["0003"],
                },
                "uno",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.method_call(
        IdentityChanges(since_state="2999", max_changes=47)
    ) == IdentityChangesResponse(
        account_id="u1138",
        old_state="2999",
        new_state="3000",
        has_more_changes=False,
        created=["0001", "0002"],
        updated=[],
        destroyed=["0003"],
    )


def test_identity_get(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [["Identity/get", {"accountId": "u1138"}, "uno"]],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:submission",
        ],
    }
    response = {
        "methodResponses": [
            [
                "Identity/get",
                {
                    "accountId": "u1138",
                    "list": [
                        {
                            "bcc": None,
                            "email": "ness@onett.example.net",
                            "htmlSignature": "",
                            "id": "0001",
                            "mayDelete": False,
                            "name": "Ness",
                            "replyTo": None,
                            "textSignature": "",
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
    assert client.method_call(IdentityGet()) == IdentityGetResponse(
        account_id="u1138",
        state="2187",
        not_found=[],
        data=[
            Identity(
                id="0001",
                name="Ness",
                email="ness@onett.example.net",
                reply_to=None,
                bcc=None,
                text_signature="",
                html_signature="",
                may_delete=False,
            )
        ],
    )


def test_identity_set(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Identity/set",
                {
                    "accountId": "u1138",
                    "create": {
                        "new_id": {
                            "name": "Mr. Saturn",
                            "email": "mr.saturn@saturn.valley.example.net",
                            "mayDelete": False,
                            "textSignature": "Boing",
                            "htmlSignature": "<i>Boing</i>",
                        }
                    },
                },
                "uno",
            ]
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:submission",
        ],
    }
    response = {
        "methodResponses": [
            [
                "Identity/set",
                {
                    "accountId": "u1138",
                    "oldState": "1",
                    "newState": "2",
                    "created": {
                        "new_id": {
                            "name": "Mr. Saturn",
                            "email": "mr.saturn@saturn.valley.example.net",
                            "mayDelete": False,
                            "textSignature": "Boing",
                            "htmlSignature": "<i>Boing</i>",
                            "replyTo": None,
                            "bcc": None,
                            "id": "0002",
                        },
                    },
                    "updated": None,
                    "destroyed": None,
                    "notCreated": None,
                    "notDestroyed": None,
                    "notUpdated": None,
                },
                "uno",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)

    assert client.method_call(
        IdentitySet(
            create=dict(
                new_id=Identity(
                    name="Mr. Saturn",
                    email="mr.saturn@saturn.valley.example.net",
                    reply_to=None,
                    bcc=None,
                    text_signature="Boing",
                    html_signature="<i>Boing</i>",
                    may_delete=False,
                )
            )
        )
    ) == IdentitySetResponse(
        account_id="u1138",
        old_state="1",
        new_state="2",
        created=dict(
            new_id=Identity(
                id="0002",
                name="Mr. Saturn",
                email="mr.saturn@saturn.valley.example.net",
                reply_to=None,
                bcc=None,
                text_signature="Boing",
                html_signature="<i>Boing</i>",
                may_delete=False,
            )
        ),
        updated=None,
        destroyed=None,
        not_created=None,
        not_updated=None,
        not_destroyed=None,
    )
