import json
import logging
import time
from typing import Iterable

import pytest
import responses

from jmapc import Client
from jmapc.logging import log

pytest.register_assert_rewrite("tests.utils")


@pytest.fixture(autouse=True)
def test_log() -> Iterable[None]:
    class UTCFormatter(logging.Formatter):
        converter = time.gmtime

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = UTCFormatter(
        "%(asctime)s %(name)-12s %(levelname)-8s "
        "[%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    log.setLevel(logging.DEBUG)
    yield


@pytest.fixture
def client() -> Iterable[Client]:
    yield Client(
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
