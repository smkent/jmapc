import json
from pathlib import Path
from typing import List, Set

import pytest
import requests
import responses

from jmapc import Blob, Client, ClientError, EmailBodyPart, constants
from jmapc.auth import BearerAuth
from jmapc.methods import (
    CoreEcho,
    CoreEchoResponse,
    Invocation,
    InvocationResponseOrError,
    MailboxGet,
    MailboxGetResponse,
    Request,
)
from jmapc.ref import Ref, ResultReference
from jmapc.session import (
    Session,
    SessionCapabilities,
    SessionCapabilitiesCore,
    SessionPrimaryAccount,
)

from .data import make_session_response
from .utils import expect_jmap_call

echo_test_data = dict(
    who="Ness", goods=["Mr. Saturn coin", "Hall of Fame Bat"]
)


@pytest.mark.parametrize(
    "test_client",
    (
        Client.create_with_api_token(
            "jmap-example.localhost", api_token="ness__pk_fire"
        ),
        Client.create_with_password(
            "jmap-example.localhost", user="ness", password="pk_fire"
        ),
        Client("jmap-example.localhost", auth=("ness", "pk_fire")),
        Client(
            "jmap-example.localhost",
            auth=requests.auth.HTTPBasicAuth(
                username="ness", password="pk_fire"
            ),
        ),
        Client("jmap-example.localhost", auth=BearerAuth("ness__pk_fire")),
    ),
)
def test_jmap_session(
    test_client: Client, http_responses: responses.RequestsMock
) -> None:
    assert test_client.jmap_session == Session(
        username="ness@onett.example.net",
        api_url="https://jmap-api.localhost/api",
        download_url=(
            "https://jmap-api.localhost/jmap/download"
            "/{accountId}/{blobId}/{name}?type={type}"
        ),
        upload_url="https://jmap-api.localhost/jmap/upload/{accountId}/",
        event_source_url=(
            "https://jmap-api.localhost/events/{types}/{closeafter}/{ping}"
        ),
        capabilities=SessionCapabilities(
            core=SessionCapabilitiesCore(
                max_size_upload=50_000_000,
                max_concurrent_upload=4,
                max_size_request=10_000_000,
                max_concurrent_requests=4,
                max_calls_in_request=16,
                max_objects_in_get=500,
                max_objects_in_set=500,
                collation_algorithms={
                    "i;ascii-numeric",
                    "i;ascii-casemap",
                    "i;octet",
                },
            )
        ),
        primary_accounts=SessionPrimaryAccount(
            core="u1138",
            mail="u1138",
            submission="u1138",
        ),
        state="test;session;state",
    )


def test_jmap_session_no_account(
    http_responses_base: responses.RequestsMock,
) -> None:
    session_response = make_session_response()
    session_response["primaryAccounts"] = {}
    http_responses_base.add(
        method=responses.GET,
        url="https://jmap-example.localhost/.well-known/jmap",
        body=json.dumps(session_response),
    )
    client = Client.create_with_api_token(
        "jmap-example.localhost", api_token="ness__pk_fire"
    )
    with pytest.raises(Exception) as e:
        client.account_id
    assert str(e.value) == "No primary account ID found"


@pytest.mark.parametrize(
    "urns",
    [
        {constants.JMAP_URN_MAIL},
        {constants.JMAP_URN_MAIL, constants.JMAP_URN_SUBMISSION},
        {
            constants.JMAP_URN_MAIL,
            constants.JMAP_URN_SUBMISSION,
            "https://jmap.example.com/extra/capability",
        },
        {
            "https://jmap.example.com/other/extra/capability",
        },
    ],
)
def test_jmap_session_capabilities_urns(
    client: Client,
    http_responses_base: responses.RequestsMock,
    urns: Set[str],
) -> None:
    session_response = make_session_response()
    session_response["capabilities"].update({u: {} for u in urns})
    http_responses_base.add(
        method=responses.GET,
        url="https://jmap-example.localhost/.well-known/jmap",
        body=json.dumps(session_response),
    )
    assert client.jmap_session.capabilities.urns == (
        {"urn:ietf:params:jmap:core"} | urns
    )


def test_client_request_updated_session(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    new_session_response = make_session_response()
    new_session_response.update(
        {
            "state": "updated;state;value",
            "username": "paula@twoson.example.net",
        }
    )
    http_responses.add(
        method=responses.GET,
        url="https://jmap-example.localhost/.well-known/jmap",
        body=json.dumps(new_session_response),
    )
    method_params = CoreEcho(data=echo_test_data)
    expected_request = {
        "methodCalls": [
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
        ],
        "using": ["urn:ietf:params:jmap:core"],
    }
    response = {
        "methodResponses": [
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
        ],
        "sessionState": "updated;state;value",
    }
    expect_jmap_call(http_responses, expected_request, response)
    expected_response = CoreEchoResponse(data=echo_test_data)
    assert client.jmap_session.username == "ness@onett.example.net"
    assert client.request(method_params) == expected_response
    assert client.jmap_session.username == "paula@twoson.example.net"


@pytest.mark.parametrize(
    "method_params",
    [
        [CoreEcho(data=echo_test_data), MailboxGet(ids=Ref("/example"))],
        [
            Invocation(method=CoreEcho(data=echo_test_data), id="0.Core/echo"),
            Invocation(
                method=MailboxGet(ids=Ref(path="/example")), id="1.Mailbox/get"
            ),
        ],
        [
            Invocation(method=CoreEcho(data=echo_test_data), id="0.Core/echo"),
            MailboxGet(ids=Ref("/example", method="0.Core/echo")),
        ],
        [
            CoreEcho(data=echo_test_data),
            MailboxGet(
                ids=ResultReference(
                    path="/example", result_of="0.Core/echo", name="Core/echo"
                )
            ),
        ],
    ],
    ids=[
        "methods_only",
        "invocations_only",
        "method_and_invocation",
        "methods_with_manual_reference",
    ],
)
def test_client_request(
    client: Client,
    http_responses: responses.RequestsMock,
    method_params: List[Request],
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Core/echo",
                echo_test_data,
                "0.Core/echo",
            ],
            [
                "Mailbox/get",
                {
                    "accountId": "u1138",
                    "#ids": {
                        "name": "Core/echo",
                        "path": "/example",
                        "resultOf": "0.Core/echo",
                    },
                },
                "1.Mailbox/get",
            ],
        ],
        "using": ["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:mail"],
    }
    response = {
        "methodResponses": [
            [
                "Core/echo",
                echo_test_data,
                "0.Core/echo",
            ],
            [
                "Mailbox/get",
                {
                    "accountId": "u1138",
                    "list": [],
                    "not_found": [],
                    "state": "1000",
                },
                "1.Mailbox/get",
            ],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(method_params) == [
        InvocationResponseOrError(
            response=CoreEchoResponse(data=echo_test_data), id="0.Core/echo"
        ),
        InvocationResponseOrError(
            response=MailboxGetResponse(
                account_id="u1138",
                not_found=[],
                data=[],
                state="1000",
            ),
            id="1.Mailbox/get",
        ),
    ]


@pytest.mark.parametrize("raise_errors", [True, False])
def test_client_request_single(
    client: Client, http_responses: responses.RequestsMock, raise_errors: bool
) -> None:
    method_params = CoreEcho(data=echo_test_data)
    expected_request = {
        "methodCalls": [
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
        ],
        "using": ["urn:ietf:params:jmap:core"],
    }
    response = {
        "methodResponses": [
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    expected_response = CoreEchoResponse(data=echo_test_data)
    if raise_errors:
        assert (
            client.request(method_params, raise_errors=True)
            == expected_response
        )
    else:
        assert (
            client.request(method_params, raise_errors=False)
            == expected_response
        )


def test_client_request_single_with_multiple_responses(
    client: Client,
    http_responses: responses.RequestsMock,
) -> None:
    method_params = CoreEcho(data=echo_test_data)
    expected_request = {
        "methodCalls": [
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
        ],
        "using": ["urn:ietf:params:jmap:core"],
    }
    response = {
        "methodResponses": [
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.request(method_params) == [
        CoreEchoResponse(data=echo_test_data),
        CoreEchoResponse(data=echo_test_data),
    ]


def test_client_request_single_with_multiple_responses_error(
    client: Client,
    http_responses: responses.RequestsMock,
) -> None:
    method_params = CoreEcho(data=echo_test_data)
    expected_request = {
        "methodCalls": [
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
        ],
        "using": ["urn:ietf:params:jmap:core"],
    }
    response = {
        "methodResponses": [
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
            [
                "Core/echo",
                echo_test_data,
                "single.Core/echo",
            ],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    with pytest.raises(ClientError) as e:
        client.request(method_params, single_response=True)
    assert (
        str(e.value)
        == "2 method responses received for single method call Core/echo"
    )
    assert e.value.result == 2 * [
        InvocationResponseOrError(
            id="single.Core/echo",
            response=CoreEchoResponse(data=echo_test_data),
        )
    ]


def test_client_invalid_single_response_argument(client: Client) -> None:
    with pytest.raises(ValueError):
        client.request(
            [CoreEcho(data=echo_test_data), MailboxGet(ids=[])],
            single_response=True,
        )  # type: ignore


def test_error_unauthorized(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    http_responses.add(
        method=responses.POST,
        url="https://jmap-api.localhost/api",
        status=401,
    )
    with pytest.raises(requests.exceptions.HTTPError) as e:
        client.request(CoreEcho(data=echo_test_data))
    assert e.value.response.status_code == 401


def test_upload_blob(
    client: Client, http_responses: responses.RequestsMock, tempdir: Path
) -> None:
    blob_content = "test upload blob content"
    source_file = tempdir / "upload.txt"
    source_file.write_text(blob_content)
    upload_response = {
        "accountId": "u1138",
        "blobId": "C2187",
        "type": "text/plain",
        "size": len(blob_content),
    }
    http_responses.add(
        method=responses.POST,
        url="https://jmap-api.localhost/jmap/upload/u1138/",
        body=json.dumps(upload_response),
    )
    response = client.upload_blob(source_file)
    assert response == Blob(
        id="C2187", type="text/plain", size=len(blob_content)
    )


def test_download_attachment(
    client: Client, http_responses: responses.RequestsMock, tempdir: Path
) -> None:
    blob_content = "test download blob content"
    http_responses.add(
        method=responses.GET,
        url=(
            "https://jmap-api.localhost/jmap/download"
            "/u1138/C2187/download.txt?type=text/plain"
        ),
        body=blob_content,
    )
    dest_file = tempdir / "download.txt"
    with pytest.raises(Exception) as e:
        client.download_attachment(
            EmailBodyPart(
                name="download.txt", blob_id="C2187", type="text/plain"
            ),
            "",
        )
    assert str(e.value) == "Destination file name is required"
    assert not dest_file.exists()
    client.download_attachment(
        EmailBodyPart(name="download.txt", blob_id="C2187", type="text/plain"),
        dest_file,
    )
    assert dest_file.read_text() == blob_content
