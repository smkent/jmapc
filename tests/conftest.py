from __future__ import annotations

import json
import logging
import tempfile
import time
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
import responses

from jmapc import Client
from jmapc.logging import log

pytest.register_assert_rewrite("tests.data", "tests.utils")

from .data import make_session_response  # noqa: E402

if TYPE_CHECKING:
    from collections.abc import Iterable


@pytest.fixture(autouse=True)
def test_log() -> None:
    class UTCFormatter(logging.Formatter):
        def converter(self, seconds: float | None) -> time.struct_time:
            return time.gmtime(seconds)

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = UTCFormatter(
        "%(asctime)s %(name)-12s %(levelname)-8s "
        "[%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    log.setLevel(logging.DEBUG)
    return


@pytest.fixture
def client() -> Client:
    return Client(host="jmap-example.localhost", auth=("ness", "pk_fire"))


@pytest.fixture
def http_responses_base() -> Iterable[responses.RequestsMock]:
    with responses.RequestsMock() as resp_mock:
        yield resp_mock


@pytest.fixture
def http_responses(
    http_responses_base: responses.RequestsMock,
) -> responses.RequestsMock:
    http_responses_base.add(
        method=responses.GET,
        url="https://jmap-example.localhost/.well-known/jmap",
        body=json.dumps(make_session_response()),
    )
    return http_responses_base


@pytest.fixture
def tempdir() -> Iterable[Path]:
    with tempfile.TemporaryDirectory(suffix=".unit_test") as td:
        yield Path(td)
