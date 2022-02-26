from dataclasses import dataclass, fields
from datetime import datetime
from typing import Any, Dict, Optional

import dataclasses_json
import dateutil.parser


def datetime_encode(dt: Optional[datetime]) -> Optional[str]:
    if not dt:
        return None
    return f"{dt.replace(tzinfo=None).isoformat()}Z"


def datetime_decode(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    return dateutil.parser.isoparse(value)


@dataclass
class ResultReference(dataclasses_json.DataClassJsonMixin):
    dataclass_json_config = dataclasses_json.config(
        letter_case=dataclasses_json.LetterCase.CAMEL,  # type: ignore
    )["dataclasses_json"]
    name: str
    path: str
    result_of: str


class JsonDataClass(dataclasses_json.DataClassJsonMixin):
    dataclass_json_config = dataclasses_json.config(
        letter_case=dataclasses_json.LetterCase.CAMEL,  # type: ignore
        undefined=dataclasses_json.Undefined.EXCLUDE,
        exclude=lambda f: f is None,  # type: ignore
    )["dataclasses_json"]

    def _fix_refs(
        self, data: Dict[str, dataclasses_json.core.Json]
    ) -> Dict[str, dataclasses_json.core.Json]:
        for k in [key for key in data.keys() if not key.startswith("#")]:
            v = data[k]
            if isinstance(v, dict):
                if len(v.keys()) == len(fields(ResultReference)):
                    try:
                        ResultReference.from_dict(v)
                        new_key = f"#{k}"
                        if new_key in data:
                            raise Exception(
                                f"Reference key {new_key} already exists"
                            )
                        data[new_key] = v
                        del data[k]
                        continue
                    except KeyError:
                        pass
                data[k] = self._fix_refs(v)
        return data

    def to_dict(
        self, *args: Any, account_id: Optional[str] = None, **kwargs: Any
    ) -> Dict[str, dataclasses_json.core.Json]:
        if account_id:
            self.account_id: Optional[str] = account_id
        result = super().to_dict(*args, **kwargs)
        result = self._fix_refs(result)
        import pprint

        pprint.pprint(result)
        return result
