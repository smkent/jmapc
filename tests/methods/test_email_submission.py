from datetime import datetime, timezone

import responses

from jmapc import Address, Client, EmailSubmission, Envelope, UndoStatus
from jmapc.methods import EmailSubmissionSet, EmailSubmissionSetResponse

from ..utils import expect_jmap_call


def test_email_submission_set(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "EmailSubmission/set",
                {
                    "accountId": "u1138",
                    "create": {
                        "emailToSend": {
                            "emailId": "#draft",
                            "identityId": "1000",
                            "envelope": {
                                "mailFrom": {
                                    "email": "ness@onett.example.com",
                                    "parameters": None,
                                },
                                "rcptTo": [
                                    {
                                        "email": "ness@onett.example.com",
                                        "parameters": None,
                                    }
                                ],
                            },
                        }
                    },
                },
                "uno",
            ]
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:submission",
        ],
    }
    response = {
        "methodResponses": [
            [
                "EmailSubmission/set",
                {
                    "accountId": "u1138",
                    "created": {
                        "emailToSend": {
                            "id": "S2000",
                            "sendAt": "1994-08-24T12:01:02Z",
                            "undoStatus": "final",
                        }
                    },
                    "updated": None,
                    "destroyed": None,
                    "oldState": "1",
                    "newState": "2",
                    "notCreated": None,
                    "notUpdated": None,
                    "notDestroyed": None,
                },
                "uno",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)

    assert client.method_call(
        EmailSubmissionSet(
            create=dict(
                emailToSend=EmailSubmission(
                    email_id="#draft",
                    identity_id="1000",
                    envelope=Envelope(
                        mail_from=Address(email="ness@onett.example.com"),
                        rcpt_to=[Address(email="ness@onett.example.com")],
                    ),
                )
            )
        )
    ) == EmailSubmissionSetResponse(
        account_id="u1138",
        old_state="1",
        new_state="2",
        created=dict(
            emailToSend=EmailSubmission(
                id="S2000",
                undo_status=UndoStatus.FINAL,
                send_at=datetime(1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc),
            ),
        ),
        updated=None,
        destroyed=None,
        not_created=None,
        not_updated=None,
        not_destroyed=None,
    )
