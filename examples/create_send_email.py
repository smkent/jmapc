#!/usr/bin/env python3

import logging
import os

from jmapc import (
    Address,
    Client,
    Email,
    EmailAddress,
    EmailBodyPart,
    EmailBodyValue,
    EmailSubmission,
    Envelope,
    Identity,
    MailboxQueryFilterCondition,
    ResultReference,
)
from jmapc.logging import log
from jmapc.methods import (
    EmailSet,
    EmailSubmissionSet,
    EmailSubmissionSetResponse,
    IdentityGet,
    MailboxGet,
    MailboxQuery,
)

TEST_EMAIL_BODY = f"""
Hello from {__file__}!

If you're reading this email in your inbox, the example worked successfully!

This email was created with the JMAP API and sent to yourself using the first
identity's email address in your account.
""".strip()

# Create and configure client
client = Client(
    host=os.environ["JMAP_HOST"],
    user=os.environ["JMAP_USER"],
    password=os.environ["JMAP_PASSWORD"],
)

# Retrieve the Mailbox ID for Drafts
results = client.method_calls(
    [
        MailboxQuery(filter=MailboxQueryFilterCondition(name="Drafts")),
        MailboxGet(
            ids=ResultReference(
                name=MailboxQuery.name(),
                path="/ids",
                result_of="0",
            ),
        ),
        IdentityGet(),
    ]
)

# From results, second result, result object, retrieve Mailbox data
mailbox_data = results[1][1].data
if not mailbox_data:
    raise Exception("Drafts not found on the server")

# From the first mailbox result, retrieve the Mailbox ID
drafts_mailbox_id = mailbox_data[0].id
assert drafts_mailbox_id

print(f"Drafts has Mailbox ID {drafts_mailbox_id}")

# From results, third result, result object, retrieve Identity data
identity_data = results[2][1].data
if not identity_data:
    raise Exception("No identities found on the server")

# Retrieve the first Identity result
identity = identity_data[0]
assert isinstance(identity, Identity)

print(f"Found identity with email address {identity.email}")

# Create and send an email
results = client.method_calls(
    [
        # Create a draft email in the Drafts mailbox
        EmailSet(
            create=dict(
                draft=Email(
                    mail_from=[
                        EmailAddress(name=identity.name, email=identity.email)
                    ],
                    to=[
                        EmailAddress(name=identity.name, email=identity.email)
                    ],
                    subject=f"Email created with jmapc's {__file__}",
                    keywords={"$draft": True},
                    mailbox_ids={drafts_mailbox_id: True},
                    body_values=dict(
                        body=EmailBodyValue(value=TEST_EMAIL_BODY)
                    ),
                    text_body=[
                        EmailBodyPart(part_id="body", type="text/plain")
                    ],
                )
            )
        ),
        # Send the created draft email, and delete from the Drafts mailbox on
        # success
        EmailSubmissionSet(
            on_success_destroy_email=["#emailToSend"],
            create=dict(
                emailToSend=EmailSubmission(
                    email_id="#draft",
                    identity_id=identity.id,
                    envelope=Envelope(
                        mail_from=Address(email=identity.email),
                        rcpt_to=[Address(email=identity.email)],
                    ),
                )
            ),
        ),
    ]
)
# Retrieve EmailSubmission/set method response from method responses
email_send_result = results[1][1]
assert isinstance(
    email_send_result, EmailSubmissionSetResponse
), f"Error sending test email: f{email_send_result}"

# Retrieve sent email metadata from EmailSubmission/set method response
sent_data = email_send_result.created["emailToSend"]

# Print sent email timestamp
print(f"Test email sent to {identity.email} at {sent_data.send_at}")

# Example output:
#
# Found the mailbox named Inbox with ID deadbeef-0000-0000-0000-000000000001
# Found identity with email address ness@onett.example.com
# Test email sent to ness@onet.example.com at 2022-01-01 12:00:00+00:00
