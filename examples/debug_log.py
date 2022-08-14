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
client = Client.create_with_api_token(
    host=os.environ["JMAP_HOST"], api_token=os.environ["JMAP_API_TOKEN"]
)

# Call JMAP API method
# The request and response JSON content will be logged to the console
client.request(CoreEcho(data=dict(hello="world")))

# Example output:
#
# DEBUG:jmapc:Sending JMAP request {"using": ["urn:ietf:params:jmap:core"], "methodCalls": [["Core/echo", {"hello": "world"}, "single.Core/echo"]]}    # noqa: E501
# DEBUG:jmapc:Received JMAP response {"methodResponses":[["Core/echo",{"hello":"world"},"single.Core/echo"]]}                                          # noqa: E501
