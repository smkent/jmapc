#!/usr/bin/env python3

import os

from jmapc import Client
from jmapc.methods import CoreEcho

# Create and configure client
client = Client(
    host=os.environ["JMAP_HOST"],
    user=os.environ["JMAP_USER"],
    password=os.environ["JMAP_PASSWORD"],
)

# Prepare a request for the JMAP Core/echo method with some sample data
method = CoreEcho(data=dict(hello="world"))

# Call JMAP API with the prepared request
result = client.call_method(method)

# Print result
print(result)

# Example output:
#
# CoreEchoResponse(data={'hello': 'world'})
