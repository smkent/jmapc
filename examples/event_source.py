#!/usr/bin/env python3

import collections
import os
from typing import Optional

from jmapc import Client, Ref, TypeState
from jmapc.methods import EmailChanges, EmailGet, EmailGetResponse

MAX_EVENTS = 5

# Create and configure client
client = Client.create_with_api_token(
    host=os.environ["JMAP_HOST"], api_token=os.environ["JMAP_API_TOKEN"]
)


# Create a callback for email state changes
def email_change_callback(
    prev_state: Optional[str], new_state: Optional[str]
) -> None:
    if not prev_state or not new_state:
        return
    results = client.request(
        [EmailChanges(since_state=prev_state), EmailGet(ids=Ref("/created"))]
    )
    email_get_response = results[1].response
    assert isinstance(email_get_response, EmailGetResponse)
    for new_email in email_get_response.data:
        to = new_email.to[0].email if new_email.to else "(unknown)"
        print(f'Received email for "{to}" with subject "{new_email.subject}"')


# Listen for events from the EventSource endpoint
all_prev_state: dict[str, TypeState] = collections.defaultdict(TypeState)
for i, event in enumerate(client.events):
    if i >= MAX_EVENTS:
        # Exit after receiving MAX_EVENTS events
        print(f"Exiting after {i} events")
        break
    for account_id, new_state in event.data.changed.items():
        prev_state = all_prev_state[account_id]
        if new_state != prev_state:
            if prev_state.email != new_state.email:
                email_change_callback(prev_state.email, new_state.email)
            all_prev_state[account_id] = new_state

# Example output:
#
# Received email for "ness@example.com" with subject "Treasure hunter's cabin"
# Received email for "ness@example.com" with subject "Watch out for The Sharks"
# Received email for "ness@example.com" with subject "Twoson road closed"
# Received email for "ness@example.com" with subject "Big footprint"
# Received email for "ness@example.com" with subject "Can you spare a Cookie?"
# Exiting after 5 events
