from __future__ import annotations

import contextlib
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, cast

import dataclasses_json
import dateutil.parser

from .ref import REF_SENTINEL_KEY, Ref, ResultReference

if TYPE_CHECKING:
    from .methods import Invocation  # pragma: no cover


def datetime_encode(dt: datetime) -> str:
    return f"{dt.replace(tzinfo=None).isoformat()}Z"


def datetime_decode(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    return dateutil.parser.isoparse(value)


class ModelToDictPostprocessor:
    def __init__(
        self, method_calls_slice: Optional[List[Invocation]] = None
    ) -> None:
        self.method_calls_slice = method_calls_slice

    def postprocess(
        self,
        data: Dict[str, dataclasses_json.core.Json],
    ) -> Dict[str, dataclasses_json.core.Json]:
        for key in [key for key in data.keys() if not key.startswith("#")]:
            value = data[key]
            if isinstance(value, dict):
                if REF_SENTINEL_KEY in value:
                    with contextlib.suppress(KeyError):
                        data = self.fix_result_reference(data, key)
                        continue
                data[key] = self.postprocess(value)
            elif (
                key == "headers"
                and isinstance(value, list)
                and len(value) > 0
                and isinstance(value[0], dict)
                and set(value[0].keys()) == {"name", "value"}
            ):
                data = self.fix_email_headers(data, key, value)
        return data

    def resolve_ref_target(self, ref: Ref) -> int:
        assert self.method_calls_slice
        if isinstance(ref.method, int):
            return ref.method
        if isinstance(ref.method, str):
            for i, m in enumerate(self.method_calls_slice):
                if m.id == ref.method:
                    return i
            raise IndexError(f'Call "{ref.method}" for reference not found')

    def ref_to_result_reference(self, ref: Ref) -> ResultReference:
        if not self.method_calls_slice:
            raise ValueError("No previous calls for reference")
        ref_target = self.resolve_ref_target(ref)
        return ResultReference(
            name=self.method_calls_slice[ref_target].method.jmap_method_name,
            path=ref.path,
            result_of=self.method_calls_slice[ref_target].id,
        )

    def fix_result_reference(
        self,
        data: Dict[str, dataclasses_json.core.Json],
        key: str,
    ) -> Dict[str, dataclasses_json.core.Json]:
        ref_type = cast(Dict[str, Any], data[key]).get(REF_SENTINEL_KEY)
        if ref_type == "ResultReference":
            rr = ResultReference.from_dict(data[key])
        elif ref_type == "Ref":
            rr = self.ref_to_result_reference(Ref.from_dict(data[key]))
        else:
            raise ValueError(
                f"Unexpected reference sentinel value: {ref_type}"
            )
        data[key] = rr.to_dict()
        # Replace existing key with #-prefixed key
        new_key = f"#{key}"
        data[new_key] = data[key]
        del data[key]
        # Remove ref sentinel key from serialized output
        new_data = data[new_key]
        assert isinstance(new_data, dict)
        del new_data[REF_SENTINEL_KEY]
        return data

    def fix_email_headers(
        self,
        data: Dict[str, dataclasses_json.core.Json],
        key: str,
        value: List[Dict[str, str]],
    ) -> Dict[str, dataclasses_json.core.Json]:
        for header in value:
            header_key = header["name"]
            header_value = header["value"]
            data[f"header:{header_key}"] = header_value
        del data[key]
        return data


class Model(dataclasses_json.DataClassJsonMixin):
    dataclass_json_config = dataclasses_json.config(
        letter_case=dataclasses_json.LetterCase.CAMEL,  # type: ignore
        undefined=dataclasses_json.Undefined.EXCLUDE,
        exclude=lambda f: f is None,  # type: ignore
    )["dataclasses_json"]

    def to_dict(
        self,
        *args: Any,
        account_id: Optional[str] = None,
        method_calls_slice: Optional[List[Invocation]] = None,
        **kwargs: Any,
    ) -> Dict[str, dataclasses_json.core.Json]:
        if account_id:
            self.account_id: Optional[str] = account_id
        todict = ModelToDictPostprocessor(method_calls_slice)
        return todict.postprocess(super().to_dict(*args, **kwargs))
