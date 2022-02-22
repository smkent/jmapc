# import json

from .jmap import JMAP
from .types.jmap import JMAPIdentityGet


def main() -> None:
    j = JMAP()
    result = j.call_method(JMAPIdentityGet(account_id=j.account_id))
    print(result)
