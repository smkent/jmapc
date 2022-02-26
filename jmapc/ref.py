from dataclasses import dataclass

import dataclasses_json


@dataclass
class ResultReference(dataclasses_json.DataClassJsonMixin):
    dataclass_json_config = dataclasses_json.config(
        letter_case=dataclasses_json.LetterCase.CAMEL,  # type: ignore
    )["dataclasses_json"]
    name: str
    path: str
    result_of: str
