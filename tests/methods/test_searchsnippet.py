import responses

from jmapc import Client, EmailQueryFilterCondition, SearchSnippet
from jmapc.methods import SearchSnippetGet, SearchSnippetGetResponse

from ..utils import expect_jmap_call


def test_search_snippet_get(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "SearchSnippet/get",
                {
                    "accountId": "u1138",
                    "emailIds": ["M1234", "M1001"],
                    "filter": {"text": "ness"},
                },
                "single.SearchSnippet/get",
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
                "SearchSnippet/get",
                {
                    "accountId": "u1138",
                    "list": [
                        {
                            "emailId": "M1234",
                            "subject": "The year is 199x...",
                            "preview": "<mark>Ness</mark> used PK Fire",
                        },
                        {
                            "emailId": "M1001",
                            "subject": None,
                            "preview": None,
                        },
                    ],
                    "not_found": [],
                },
                "single.SearchSnippet/get",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    jmap_response = client.request(
        SearchSnippetGet(
            ids=["M1234", "M1001"],
            filter=EmailQueryFilterCondition(text="ness"),
        )
    )
    assert jmap_response == SearchSnippetGetResponse(
        account_id="u1138",
        not_found=[],
        data=[
            SearchSnippet(
                email_id="M1234",
                subject="The year is 199x...",
                preview="<mark>Ness</mark> used PK Fire",
            ),
            SearchSnippet(email_id="M1001"),
        ],
    )
    assert isinstance(jmap_response, SearchSnippetGetResponse)
