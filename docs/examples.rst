Examples
========

This page contains practical examples of using jmapc for common JMAP operations.
All examples assume you have set the ``JMAP_HOST`` and ``JMAP_API_TOKEN`` environment variables.

Basic Echo Test
---------------

The simplest way to test your connection is using the Core/echo method:

.. code-block:: python

   #!/usr/bin/env python3

   import os
   from jmapc import Client
   from jmapc.methods import CoreEcho

   # Create and configure client
   client = Client.create_with_api_token(
       host=os.environ["JMAP_HOST"], 
       api_token=os.environ["JMAP_API_TOKEN"]
   )

   # Prepare a request for the JMAP Core/echo method with some sample data
   method = CoreEcho(data=dict(hello="world"))

   # Call JMAP API with the prepared request
   result = client.request(method)

   # Print result
   print(result)
   # Output: CoreEchoResponse(data={'hello': 'world'})

Getting Identities
-------------------

Retrieve all email identities associated with your account:

.. code-block:: python

   #!/usr/bin/env python3

   import os
   from jmapc import Client
   from jmapc.methods import IdentityGet, IdentityGetResponse

   # Create and configure client
   client = Client.create_with_api_token(
       host=os.environ["JMAP_HOST"], 
       api_token=os.environ["JMAP_API_TOKEN"]
   )

   # Prepare Identity/get request
   # To retrieve all of the user's identities, no arguments are required.
   method = IdentityGet()

   # Call JMAP API with the prepared request
   result = client.request(method)

   # Print some information about each retrieved identity
   assert isinstance(result, IdentityGetResponse), "Error in Identity/get method"
   for identity in result.data:
       print(f"Identity {identity.id} is for {identity.name} at {identity.email}")

Working with Mailboxes
----------------------

Get all mailboxes and their properties:

.. code-block:: python

   import os
   from jmapc import Client
   from jmapc.methods import MailboxGet

   client = Client.create_with_api_token(
       host=os.environ["JMAP_HOST"],
       api_token=os.environ["JMAP_API_TOKEN"]
   )

   # Get all mailboxes
   mailboxes_result = client.request(MailboxGet())

   for mailbox in mailboxes_result.data:
       print(f"Mailbox: {mailbox.name}")
       print(f"  Role: {mailbox.role}")
       print(f"  Total emails: {mailbox.total_emails}")
       print(f"  Unread emails: {mailbox.unread_emails}")
       print(f"  Parent: {mailbox.parent_id}")
       print("---")

Querying and Retrieving Emails
-------------------------------

Search for emails and retrieve their details:

.. code-block:: python

   import os
   from jmapc import Client
   from jmapc.methods import EmailQuery, EmailGet
   from jmapc.models.email import EmailFilterCondition

   client = Client.create_with_api_token(
       host=os.environ["JMAP_HOST"],
       api_token=os.environ["JMAP_API_TOKEN"]
   )

   # First, find the inbox mailbox ID
   mailboxes = client.request(MailboxGet())
   inbox_id = None
   for mailbox in mailboxes.data:
       if mailbox.role == "inbox":
           inbox_id = mailbox.id
           break

   if inbox_id:
       # Query for recent emails in inbox
       email_query = client.request(EmailQuery(
           filter=EmailFilterCondition(in_mailbox=inbox_id),
           sort=[{"property": "receivedAt", "isAscending": False}],
           limit=10
       ))

       if email_query.ids:
           # Get the email details
           emails = client.request(EmailGet(
               ids=email_query.ids,
               properties=["id", "subject", "from", "receivedAt", "hasAttachment"]
           ))

           for email in emails.data:
               from_address = email.from_[0].email if email.from_ else "Unknown"
               print(f"Subject: {email.subject}")
               print(f"From: {from_address}")
               print(f"Received: {email.received_at}")
               print(f"Has attachment: {email.has_attachment}")
               print("---")

Creating and Sending Emails
----------------------------

Create a new email and send it:

.. code-block:: python

   import os
   from jmapc import Client
   from jmapc.methods import EmailSet, EmailSubmissionSet, IdentityGet
   from jmapc.models.email import Email, EmailAddress, EmailBodyPart
   from jmapc.models.emailsubmission import EmailSubmission, Envelope
   from datetime import datetime

   client = Client.create_with_api_token(
       host=os.environ["JMAP_HOST"],
       api_token=os.environ["JMAP_API_TOKEN"]
   )

   # Get the first identity to use as sender
   identities = client.request(IdentityGet())
   sender_identity = identities.data[0]

   # Create email object
   email = Email(
       from_=[EmailAddress(name=sender_identity.name, email=sender_identity.email)],
       to=[EmailAddress(email="recipient@example.com")],
       subject="Test email from jmapc",
       body_values={
           "text": EmailBodyPart(
               value="Hello from jmapc!\n\nThis is a test email.",
               type="text/plain"
           )
       },
       text_body=[{"partId": "text", "type": "text/plain"}],
       sent_at=datetime.now()
   )

   # Create the email
   email_result = client.request(EmailSet(
       account_id=client.account_id,
       create={"draft": email}
   ))

   if email_result.created:
       email_id = email_result.created["draft"].id
       
       # Submit the email for sending
       submission = EmailSubmission(
           identity_id=sender_identity.id,
           email_id=email_id,
           envelope=Envelope(
               mail_from=EmailAddress(email=sender_identity.email),
               rcpt_to=[EmailAddress(email="recipient@example.com")]
           )
       )

       submission_result = client.request(EmailSubmissionSet(
           account_id=client.account_id,
           create={"send": submission}
       ))

       if submission_result.created:
           print("Email sent successfully!")
       else:
           print("Failed to send email:", submission_result.not_created)
   else:
       print("Failed to create email:", email_result.not_created)

Using Combined Requests
-----------------------

Combine multiple operations in a single request for efficiency:

.. code-block:: python

   import os
   from jmapc import Client, Request, ResultReference
   from jmapc.methods import MailboxGet, EmailQuery, EmailGet

   client = Client.create_with_api_token(
       host=os.environ["JMAP_HOST"],
       api_token=os.environ["JMAP_API_TOKEN"]
   )

   # Create a combined request
   request = Request()

   # Add multiple method calls
   request.add_call(MailboxGet(), "mailboxes")
   request.add_call(EmailQuery(
       filter={"inMailbox": "#mailboxes/list/0/id"},  # Reference first mailbox
       limit=5
   ), "emailQuery")
   request.add_call(EmailGet(
       ids=ResultReference("emailQuery", "ids"),
       properties=["id", "subject", "from"]
   ), "emails")

   # Execute the combined request
   response = client.request(request)

   # Access results by call ID
   mailboxes = response["mailboxes"]
   emails = response["emails"]

   print(f"Found {len(emails.data)} emails in {mailboxes.data[0].name}")

Event Source Monitoring
------------------------

Monitor real-time changes using EventSource:

.. code-block:: python

   import os
   from jmapc import Client

   client = Client.create_with_api_token(
       host=os.environ["JMAP_HOST"],
       api_token=os.environ["JMAP_API_TOKEN"]
   )

   print("Monitoring for changes... (Press Ctrl+C to stop)")

   try:
       for event in client.events:
           print(f"State change: {event.changed}")
           # You can then query for specific changes based on the event
   except KeyboardInterrupt:
       print("Monitoring stopped.")

File Upload and Download
------------------------

Upload a file and download email attachments:

.. code-block:: python

   import os
   from jmapc import Client
   from jmapc.methods import EmailGet

   client = Client.create_with_api_token(
       host=os.environ["JMAP_HOST"],
       api_token=os.environ["JMAP_API_TOKEN"]
   )

   # Upload a file
   blob = client.upload_blob("document.pdf")
   print(f"Uploaded file: {blob.blob_id} ({blob.size} bytes)")

   # Download an attachment (assuming you have an email with attachments)
   email_id = "your_email_id_here"
   email = client.request(EmailGet(
       ids=[email_id],
       properties=["attachments"],
       body_properties=["blobId", "name", "type"]
   ))

   if email.data and email.data[0].attachments:
       attachment = email.data[0].attachments[0]
       client.download_attachment(attachment, f"downloaded_{attachment.name}")
       print(f"Downloaded attachment: {attachment.name}")

Running the Examples
--------------------

To run these examples:

1. Set your environment variables:

   .. code-block:: console

      export JMAP_HOST="jmap.example.com"
      export JMAP_API_TOKEN="your_api_token_here"

2. Save any example to a Python file (e.g., ``example.py``)

3. Run it:

   .. code-block:: console

      python example.py

The complete examples are also available in the ``examples/`` directory of the jmapc repository. 