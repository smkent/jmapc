#!/usr/bin/env python3

import logging
import os

from jmapc import Client
from jmapc.logging import log
from jmapc.methods import CoreEcho

# Create basic console logger
logging.basicConfig()

# Set jmapc log level to DEBUG
log.setLevel(logging.DEBUG)

# Create and configure client
client = Client(
    host=os.environ["JMAP_HOST"],
    user=os.environ["JMAP_USER"],
    password=os.environ["JMAP_PASSWORD"],
)

# Call JMAP API method
# The request and response JSON content will be logged to the console
client.method_call(CoreEcho(data=dict(hello="world")))

# Example output:
#
# DEBUG:jmapc:Sending JMAP request {"using": ["urn:ietf:params:jmap:core"], "methodCalls": [["Core/echo", {"hello": "world"}, "uno"]]}    # noqa: E501
# DEBUG:jmapc:Received JMAP response {"methodResponses":[["Core/echo",{"hello":"world"},"uno"]]}                                          # noqa: E501
