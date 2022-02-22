from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin, config

from .. import constants


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


class JMAPCall(DataClassJsonMixin):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def using(self) -> set[str]:
        pass


@dataclass
class JMAPCallIdentityGet(JMAPCall):
    @property
    def name(self) -> str:
        return "Identity/get"

    @property
    def using(self) -> set[str]:
        return set([constants.JMAP_URN_SUBMISSION])

    account_id: str = field(metadata=config(field_name="accountId"))
