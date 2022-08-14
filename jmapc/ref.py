from dataclasses import dataclass, field
from typing import Union

import dataclasses_json
from dataclasses_json import config

REF_SENTINEL_KEY = "__ref"


@dataclass
class ResultReference(dataclasses_json.DataClassJsonMixin):
    dataclass_json_config = dataclasses_json.config(
        letter_case=dataclasses_json.LetterCase.CAMEL,  # type: ignore
    )["dataclasses_json"]
    name: str
    path: str
    result_of: str
    _ref_sentinel: str = field(
        init=False,
        default="ResultReference",
        metadata=config(field_name=REF_SENTINEL_KEY),
    )


@dataclass
class Ref(dataclasses_json.DataClassJsonMixin):
    path: str
    method: Union[str, int] = -1
    _ref_sentinel: str = field(
        init=False,
        default="Ref",
        metadata=config(field_name=REF_SENTINEL_KEY),
    )
