import responses

from jmapc import Client, Mailbox, Ref, constants
from jmapc.methods import (
    CustomMethod,
    CustomResponse,
    InvocationResponseOrError,
    MailboxGet,
    MailboxGetResponse,
)

from ..utils import expect_jmap_call


def test_custom_method(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    test_data = dict(
        accountId="u1138",
        custom_value="Spiteful Crow",
        list_value=["ness", "paula", "jeff", "poo"],
    )
    expected_request = {
        "methodCalls": [
            [
                "Custom/method",
                test_data,
                "single.Custom/method",
            ],
        ],
        "using": ["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:mail"],
    }
    response = {
        "methodResponses": [
            [
                "Custom/method",
                test_data,
                "single.Custom/method",
            ],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    method = CustomMethod(data=test_data)
    method.jmap_method = "Custom/method"
    method.using = {constants.JMAP_URN_MAIL}
    assert method.to_dict() == test_data
    resp = client.request(method)
    assert resp == CustomResponse(account_id="u1138", data=test_data)


def test_custom_method_as_result_reference_target(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    test_data = dict(
        accountId="u1138",
        custom_value="Spiteful Crow",
        list_value=["ness", "paula", "jeff", "poo"],
    )
    expected_request = {
        "methodCalls": [
            [
                "Custom/method",
                test_data,
                "0.Custom/method",
            ],
            [
                "Mailbox/get",
                {
                    "accountId": "u1138",
                    "#ids": {
                        "name": "Custom/method",
                        "path": "/example",
                        "resultOf": "0.Custom/method",
                    },
                },
                "1.Mailbox/get",
            ],
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:mail",
        ],
    }
    response = {
        "methodResponses": [
            [
                "Custom/method",
                test_data,
                "0.Custom/method",
            ],
            [
                "Mailbox/get",
                {
                    "accountId": "u1138",
                    "list": [
                        {
                            "id": "MBX1",
                            "name": "First",
                            "sortOrder": 1,
                            "totalEmails": 100,
                            "unreadEmails": 3,
                            "totalThreads": 5,
                            "unreadThreads": 1,
                            "isSubscribed": True,
                        },
                    ],
                    "not_found": [],
                    "state": "2187",
                },
                "1.Mailbox/get",
            ],
        ],
    }
    expect_jmap_call(http_responses, expected_request, response)
    method = CustomMethod(data=test_data)
    method.jmap_method = "Custom/method"
    method.using = {constants.JMAP_URN_MAIL}
    assert method.to_dict() == test_data
    resp = client.request([method, MailboxGet(ids=Ref("/example"))])
    assert resp == [
        InvocationResponseOrError(
            response=CustomResponse(account_id="u1138", data=test_data),
            id="0.Custom/method",
        ),
        InvocationResponseOrError(
            response=MailboxGetResponse(
                account_id="u1138",
                state="2187",
                not_found=[],
                data=[
                    Mailbox(
                        id="MBX1",
                        name="First",
                        sort_order=1,
                        total_emails=100,
                        unread_emails=3,
                        total_threads=5,
                        unread_threads=1,
                        is_subscribed=True,
                    ),
                ],
            ),
            id="1.Mailbox/get",
        ),
    ]
