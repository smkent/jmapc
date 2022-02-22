from __future__ import annotations

from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin, config

from ... import constants


@dataclass
class JMAPSession(DataClassJsonMixin):
    username: str
    api_url: str = field(metadata=config(field_name="apiUrl"))
    primary_accounts: JMAPSessionPrimaryAccount = field(
        metadata=config(field_name="primaryAccounts")
    )


@dataclass
class JMAPSessionPrimaryAccount(DataClassJsonMixin):
    core: str = field(metadata=config(field_name=constants.JMAP_URN_CORE))
    mail: str = field(metadata=config(field_name=constants.JMAP_URN_MAIL))
    submission: str = field(
        metadata=config(field_name=constants.JMAP_URN_SUBMISSION)
    )
