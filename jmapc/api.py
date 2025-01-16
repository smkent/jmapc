from __future__ import annotations

from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Union,
    cast,
)
from collections.abc import Sequence

from dataclasses_json import config

from . import constants, errors
from .methods import (
    CustomResponse,
    Invocation,
    InvocationResponseOrError,
    Method,
    Request,
    Response,
    ResponseOrError,
)
from .serializer import Model


def decode_method_responses(
    value: Sequence[tuple[str, dict[str, Any], str]],
) -> list[InvocationResponseOrError]:
    def _response_type(method_name: str) -> type[ResponseOrError]:
        if method_name == "error":
            return errors.Error
        return Response.response_types.get(method_name, CustomResponse)

    return [
        InvocationResponseOrError(
            id=method_id,
            response=_response_type(name).from_dict(response),
        )
        for name, response, method_id in value
    ]


@dataclass
class APIResponse(Model):
    session_state: str
    method_responses: list[InvocationResponseOrError] = field(
        metadata=config(
            encoder=lambda value: None,
            decoder=decode_method_responses,
        ),
    )
    created_ids: list[str] = field(default_factory=list)


@dataclass
class APIRequest(Model):
    account_id: str = field(
        repr=False,
        metadata=config(exclude=cast(Callable[..., bool], lambda *_: True)),
    )
    method_calls: list[tuple[str, Any, str]]
    using: set[str] = field(
        init=False,
        default_factory=lambda: {constants.JMAP_URN_CORE},
        metadata=config(encoder=lambda value: sorted(list(value))),
    )

    @staticmethod
    def from_calls(
        account_id: str,
        calls: Union[Sequence[Request], Sequence[Method], Method],
    ) -> APIRequest:
        calls_list = calls if isinstance(calls, Sequence) else [calls]
        invocations: list[Invocation] = []
        # Create Invocations for Methods
        for i, c in enumerate(calls_list):
            if isinstance(c, Invocation):
                invocations.append(c)
                continue
            call_id = i if len(calls_list) > 1 else "single"
            invocations.append(
                Invocation(id=f"{call_id}.{c.jmap_method_name}", method=c)
            )
        # Build method calls list from Invocations
        method_calls = [
            (
                c.method.jmap_method_name,
                c.method.to_dict(
                    account_id=account_id,
                    method_calls_slice=invocations[:i],
                    encode_json=False,
                ),
                c.id,
            )
            for i, c in enumerate(invocations)
        ]
        api_request = APIRequest(
            account_id=account_id, method_calls=method_calls
        )
        api_request.using |= {c.method.using for c in invocations}
        return api_request
