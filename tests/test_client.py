import responses

from jmapc import Client
from jmapc.session import Session, SessionPrimaryAccount


def test_identity_get(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    assert client.session == Session(
        username="ness@onett.example.net",
        api_url="https://jmap-api.localhost/api",
        primary_accounts=SessionPrimaryAccount(
            core="u1138",
            mail="u1138",
            submission="u1138",
        ),
    )
