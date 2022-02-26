#!/usr/bin/env python3

import os

from jmapc import Client, MailboxQueryFilterCondition, ResultReference
from jmapc.methods import MailboxGet, MailboxQuery

# Create and configure client
client = Client(
    host=os.environ["JMAP_HOST"],
    user=os.environ["JMAP_USER"],
    password=os.environ["JMAP_PASSWORD"],
)

# Prepare two methods to be submitted in one request
# The first method, Mailbox/query, will locate the ID of the Inbox folder
# The second method, Mailbox/get, uses a result reference to retrieve the Inbox
# mailbox details
methods = [
    MailboxQuery(filter=MailboxQueryFilterCondition(name="Inbox")),
    MailboxGet(
        ids=ResultReference(
            name=MailboxQuery.name(),
            path="/ids",
            result_of="0",
        ),
    ),
]

# Call JMAP API with the prepared request
results = client.call_methods(methods)

# Retrieve the result tuple for the second method. The result tuple contains
# the client-provided method ID, and the result data model.
method_2_result = results[1]

# Retrieve the result data model from the result tuple
method_2_result_data = method_2_result[1]

# Retrieve the Mailbox data from the result data model
mailboxes = method_2_result_data.data

# Although multiple mailboxes may be present in the results, we only expect a
# single match for our query. Retrieve the first Mailbox from the list.
mailbox = mailboxes[0]

# Print some information about the mailbox
print(f"Found the mailbox named {mailbox.name} with ID {mailbox.id}")
print(
    f"This mailbox has {mailbox.total_emails} emails, "
    f"{mailbox.unread_emails} of which are unread"
)

# Example output:
#
# Found the mailbox named Inbox with ID deadbeef-0000-0000-0000-000000000001
# This mailbox has 42 emails, 4 of which are unread
