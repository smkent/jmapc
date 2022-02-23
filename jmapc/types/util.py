import dataclasses_json

from typing import Optional, Dict, Any


class JsonDataClass(dataclasses_json.DataClassJsonMixin):
    dataclass_json_config = dataclasses_json.config(
        letter_case=dataclasses_json.LetterCase.CAMEL,  # type: ignore
        undefined=dataclasses_json.Undefined.EXCLUDE,
        exclude=lambda f: f is None,  # type: ignore
    )["dataclasses_json"]
    pass

    def to_dict(
        self, *args: Any, account_id: Optional[str] = None, **kwargs: Any
    ) -> Dict[str, dataclasses_json.core.Json]:
        if account_id:
            self.account_id: Optional[str] = account_id
        return super().to_dict(*args, **kwargs)
