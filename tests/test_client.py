import json
from typing import Iterable

import pytest
import responses

from jmapc import Identity, JMAPClient, ResultReference
from jmapc.client import MethodList
from jmapc.methods import IdentityGet, IdentityGetResponse


@pytest.fixture
def jmap() -> Iterable[JMAPClient]:
    yield JMAPClient(
        host="jmap-example.localhost",
        user="ness",
        password="pk_fire",
    )


@pytest.fixture
def http_responses() -> Iterable[responses.RequestsMock]:
    with responses.RequestsMock() as resp_mock:
        resp_mock.add(
            method=responses.GET,
            url="https://jmap-example.localhost/.well-known/jmap",
            body=json.dumps(
                {
                    "apiUrl": "https://jmap-api.localhost/api",
                    "username": "ness@onett.example.net",
                    "primary_accounts": {
                        "urn:ietf:params:jmap:core": "u1138",
                        "urn:ietf:params:jmap:mail": "u1138",
                        "urn:ietf:params:jmap:submission": "u1138",
                    },
                },
            ),
        )
        yield resp_mock


def test_identity_get(
    jmap: JMAPClient, http_responses: responses.RequestsMock
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
    resp = jmap.call_methods(args)
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
    print(resp)
