from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Sequence, Tuple, Type

from dataclasses_json import config

from . import errors
from .methods import (
    CustomResponse,
    InvocationResponseOrError,
    Response,
    ResponseOrError,
)
from .serializer import Model


def decode_method_responses(
    value: Sequence[Tuple[str, Dict[str, Any], str]],
) -> List[InvocationResponseOrError]:
    def _response_type(method_name: str) -> Type[ResponseOrError]:
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
    method_responses: List[InvocationResponseOrError] = field(
        metadata=config(
            encoder=lambda value: None,
            decoder=decode_method_responses,
        ),
    )
    created_ids: List[str] = field(default_factory=list)
