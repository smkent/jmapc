import json
from typing import Iterable, Optional
from unittest import mock

import pytest
import responses
import sseclient

from jmapc import Client, Event, EventSourceConfig, StateChange, TypeState

from .data import make_session_response


@pytest.fixture
def mock_sseclient() -> Iterable[mock.MagicMock]:
    mock_client = mock.MagicMock(
        spec=sseclient.SSEClient,
        __iter__=lambda self: self,
        __next__=mock.MagicMock(side_effect=[None]),
    )
    with mock.patch.object(
        sseclient,
        "SSEClient",
        mock_client,
    ):
        assert isinstance(sseclient.SSEClient, mock.MagicMock)
        sseclient.SSEClient.return_value.__iter__.side_effect = (
            lambda: sseclient.SSEClient.return_value
        )
        sseclient.SSEClient.return_value.__next__.side_effect = []
        yield mock_client


@pytest.mark.parametrize(
    ["event_source_url", "expected_call_url", "event_source_config"],
    [
        (
            "https://jmap-api.localhost/events/{types}/{closeafter}/{ping}",
            "https://jmap-api.localhost/events/*/no/0",
            None,
        ),
        (
            "https://jmap-api.localhost/events/{types}/{closeafter}/{ping}",
            "https://jmap-api.localhost/events/Email,CalendarEvent/state/37",
            EventSourceConfig(
                types="Email,CalendarEvent", closeafter="state", ping=37
            ),
        ),
        (
            "https://jmap-api.localhost/events/{ping}",
            "https://jmap-api.localhost/events/0",
            None,
        ),
        (
            "https://jmap-api.localhost/events/{ping}",
            "https://jmap-api.localhost/events/299",
            EventSourceConfig(ping=299),
        ),
        (
            "https://jmap-api.localhost/events/",
            "https://jmap-api.localhost/events/",
            None,
        ),
    ],
)
def test_event_source_url(
    mock_sseclient: mock.MagicMock,
    event_source_url: str,
    expected_call_url: str,
    event_source_config: Optional[EventSourceConfig],
) -> None:
    client = Client(
        host="jmap-example.localhost",
        auth=("ness", "pk_fire"),
        event_source_config=event_source_config,
    )
    with responses.RequestsMock() as resp_mock:
        session_response = make_session_response()
        session_response["eventSourceUrl"] = event_source_url
        resp_mock.add(
            method=responses.GET,
            url="https://jmap-example.localhost/.well-known/jmap",
            body=json.dumps(session_response),
        )
        with pytest.raises(StopIteration):
            next(client.events)
        mock_sseclient.assert_called_once_with(
            expected_call_url,
            auth=("ness", "pk_fire"),
            last_id=None,
        )


def test_event_source(
    client: Client,
    mock_sseclient: mock.MagicMock,
    http_responses: responses.RequestsMock,
) -> None:
    mock_events = [
        sseclient.Event(
            id="8001",
            event="state",
            data=json.dumps({"changed": {"u1138": {"Email": "1001"}}}),
        ),
        sseclient.Event(
            id="8001.5",
            event="ping",
            data="ignore-me",
        ),
        sseclient.Event(
            id="8002",
            event="state",
            data=json.dumps(
                {
                    "changed": {
                        "u1138": {
                            "CalendarEvent": "1011",
                            "Email": "1001",
                            "EmailDelivery": "1003",
                            "Mailbox": "1021",
                            "Thread": "1020",
                        }
                    }
                }
            ),
        ),
        sseclient.Event(
            id="",
            event="ping",
            data="also-ignore-me",
        ),
        sseclient.Event(
            event="state",
            data=json.dumps(
                {"changed": {"u1138": {"Email": "2000", "Mailbox": "2222"}}}
            ),
        ),
    ]
    expected_events = [
        Event(
            id="8001",
            data=StateChange(changed={"u1138": TypeState(email="1001")}),
        ),
        Event(
            id="8002",
            data=StateChange(
                changed={
                    "u1138": TypeState(
                        calendar_event="1011",
                        email="1001",
                        email_delivery="1003",
                        mailbox="1021",
                        thread="1020",
                    )
                }
            ),
        ),
        Event(
            id=None,
            data=StateChange(
                changed={
                    "u1138": TypeState(
                        email="2000",
                        mailbox="2222",
                    )
                }
            ),
        ),
    ]
    assert isinstance(sseclient.SSEClient, mock.MagicMock)
    sseclient.SSEClient.return_value.__next__.side_effect = mock_events
    for expected_event in expected_events:
        event = next(client.events)
        assert event == expected_event
    with pytest.raises(StopIteration):
        next(client.events)
    mock_sseclient.assert_called_once_with(
        "https://jmap-api.localhost/events/*/no/0",
        auth=("ness", "pk_fire"),
        last_id=None,
    )
