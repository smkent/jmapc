import responses

from jmapc import Client, Thread
from jmapc.methods import ThreadGet, ThreadGetResponse

from ..utils import expect_jmap_call


def test_identity_get(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "Thread/get",
                {"accountId": "u1138", "ids": ["T1", "T1000"]},
                "uno",
            ]
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:mail",
        ],
    }
    response = {
        "methodResponses": [
            [
                "Thread/get",
                {
                    "accountId": "u1138",
                    "list": [
                        {
                            "id": "T1",
                            "emailIds": [
                                "M1234",
                                "M2345",
                                "M3456",
                            ],
                        },
                        {
                            "id": "T1000",
                            "emailIds": [
                                "M1001",
                            ],
                        },
                    ],
                    "not_found": [],
                    "state": "2187",
                },
                "uno",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.method_call(
        ThreadGet(ids=["T1", "T1000"])
    ) == ThreadGetResponse(
        account_id="u1138",
        state="2187",
        not_found=[],
        data=[
            Thread(
                id="T1",
                email_ids=["M1234", "M2345", "M3456"],
            ),
            Thread(
                id="T1000",
                email_ids=["M1001"],
            ),
        ],
    )
