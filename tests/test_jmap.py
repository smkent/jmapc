import json
import os
from typing import Iterable
from unittest import mock

import pytest
import responses

from jmapc.jmap import JMAP
from jmapc.types.jmap import (
    JMAPIdentity,
    JMAPIdentityGet,
    JMAPIdentityGetResponse,
    JMAPResultReference,
)


@pytest.fixture(autouse=True)
def os_environ() -> Iterable[None]:
    mock_environ = dict(
        JMAP_HOSTNAME="jmap-example.localhost",
        JMAP_USERNAME="ness",
        JMAP_PASSWORD="pk_fire",
    )
    with mock.patch.object(os, "environ", mock_environ) as _:
        yield


@pytest.fixture
def jmap() -> Iterable[JMAP]:
    yield JMAP()


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
    jmap: JMAP, http_responses: responses.RequestsMock
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
    resp = jmap.call_methods(
        [
            ("0", JMAPIdentityGet(ids=None)),
            (
                "1",
                JMAPIdentityGet(
                    ids=JMAPResultReference(
                        name=JMAPIdentityGet.name(),
                        path="/ids",
                        result_of="0",
                    )
                ),
            ),
        ]
    )
    assert resp == [
        (
            "0",
            JMAPIdentityGetResponse(
                account_id="u1138",
                state="2187",
                not_found=[],
                data=[
                    JMAPIdentity(
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
