import responses

from jmapc import Client, Identity
from jmapc.methods import IdentityGet, IdentityGetResponse

from ..utils import expect_jmap_call


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
