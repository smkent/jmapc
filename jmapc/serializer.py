from dataclasses import fields
from datetime import datetime
from typing import Any, Dict, List, Optional

import dataclasses_json
import dateutil.parser

from .ref import REF_SENTINEL, Ref, ResultReference


def datetime_encode(dt: datetime) -> str:
    return f"{dt.replace(tzinfo=None).isoformat()}Z"


def datetime_decode(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    return dateutil.parser.isoparse(value)


class Model(dataclasses_json.DataClassJsonMixin):
    dataclass_json_config = dataclasses_json.config(
        letter_case=dataclasses_json.LetterCase.CAMEL,  # type: ignore
        undefined=dataclasses_json.Undefined.EXCLUDE,
        exclude=lambda f: f is None,  # type: ignore
    )["dataclasses_json"]

    def _fix_result_ref(
        self,
        data: Dict[str, dataclasses_json.core.Json],
        key: str,
        method_calls_slice: Optional[List[Any]] = None,
    ) -> Dict[str, dataclasses_json.core.Json]:
        ref_type = data[key].get(REF_SENTINEL)
        if ref_type == "ResultReference":
            rr = ResultReference.from_dict(data[key])
        elif ref_type == "Ref":
            r = Ref.from_dict(data[key])
            rr = ResultReference(
                name=method_calls_slice[r.method_call_index].call.name,
                path=r.path,
                result_of=method_calls_slice[r.method_call_index].id,
            )
        else:
            return data
        data[key] = rr.to_dict()
        new_key = f"#{key}"
        data[new_key] = data[key]
        del data[key]
        assert isinstance(data[new_key], dict)
        del data[new_key]["__ref"]
        return data

    def _fix_headers(
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

    def _postprocess(
        self,
        data: Dict[str, dataclasses_json.core.Json],
        method_calls_slice: Optional[List[Any]] = None,
    ) -> Dict[str, dataclasses_json.core.Json]:
        for key in [key for key in data.keys() if not key.startswith("#")]:
            value = data[key]
            if isinstance(value, dict):
                if REF_SENTINEL in value:
                    try:
                        data = self._fix_result_ref(
                            data, key, method_calls_slice=method_calls_slice
                        )
                        continue
                    except KeyError:
                        pass
                data[key] = self._postprocess(value)
            elif (
                key == "headers"
                and isinstance(value, list)
                and len(value) > 0
                and isinstance(value[0], dict)
                and set(value[0].keys()) == set(["name", "value"])
            ):
                data = self._fix_headers(data, key, value)
        return data

    def to_dict(
        self,
        *args: Any,
        account_id: Optional[str] = None,
        method_calls_slice: Optional[List[Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, dataclasses_json.core.Json]:
        if account_id:
            self.account_id: Optional[str] = account_id
        result = super().to_dict(*args, **kwargs)
        result = self._postprocess(result, method_calls_slice)
        return result
