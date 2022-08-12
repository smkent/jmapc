from dataclasses import dataclass, field

import dataclasses_json
from dataclasses_json import config

REF_SENTINEL = "__ref"


@dataclass
class ResultReference(dataclasses_json.DataClassJsonMixin):
    dataclass_json_config = dataclasses_json.config(
        letter_case=dataclasses_json.LetterCase.CAMEL,  # type: ignore
    )["dataclasses_json"]
    name: str
    path: str
    result_of: str
    internal_ref: str = field(
        init=False,
        default="ResultReference",
        metadata=config(field_name=REF_SENTINEL),
    )


@dataclass
class Ref(dataclasses_json.DataClassJsonMixin):
    path: str
    method_call_index: int = -1
    internal_ref: str = field(
        init=False,
        default="Ref",
        metadata=config(field_name=REF_SENTINEL),
    )
