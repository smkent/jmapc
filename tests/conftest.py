from typing import Iterable

import pytest

from jmapc import Client


@pytest.fixture
def client() -> Iterable[Client]:
    yield Client(
        host="jmap-example.localhost",
        user="ness",
        password="pk_fire",
    )
