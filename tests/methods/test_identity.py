import json

import responses

from jmapc import Client, Identity, ResultReference
from jmapc.client import MethodList
from jmapc.methods import IdentityGet, IdentityGetResponse


def test_identity_get(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    http_responses.add(
        method=responses.POST,
        url="https://jmap-api.localhost/api",
        body=json.dumps(
            {
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
                        "0",
                    ],
                ],
            },
        ),
    )
    args: MethodList = [
        ("0", IdentityGet(ids=None)),
        (
            "1",
            IdentityGet(
                ids=ResultReference(
                    name=IdentityGet.name(),
                    path="/ids",
                    result_of="0",
                )
            ),
        ),
    ]
    resp = client.call_methods(args)
    assert resp == [
        (
            "0",
            IdentityGetResponse(
                account_id="u1138",
                state="2187",
                not_found=[],
                data=[
                    Identity(
                        id="0001",
                        name="Ness",
                        email="ness@onett.example.net",
                        replyTo=None,
                        bcc=None,
                        textSignature="",
                        htmlSignature="",
                        mayDelete=False,
                    )
                ],
            ),
        ),
    ]
