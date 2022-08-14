#!/usr/bin/env python3

import os

from jmapc import Client
from jmapc.methods import CoreEcho

# Create and configure client
client = Client.create_with_api_token(
    host=os.environ["JMAP_HOST"], api_token=os.environ["JMAP_API_TOKEN"]
)

# Prepare a request for the JMAP Core/echo method with some sample data
method = CoreEcho(data=dict(hello="world"))

# Call JMAP API with the prepared request
result = client.request(method)

# Print result
print(result)

# Example output:
#
# CoreEchoResponse(data={'hello': 'world'})
