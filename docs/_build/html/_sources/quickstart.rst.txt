Quick Start
===========

This guide will help you get started with jmapc quickly.

Basic Usage
-----------

First, you need to create a client instance. There are several ways to authenticate:

**Using an API Token (Recommended):**

.. code-block:: python

   import jmapc

   client = jmapc.Client.create_with_api_token(
       host="jmap.example.com",
       api_token="your_api_token_here"
   )

**Using Username and Password:**

.. code-block:: python

   import jmapc

   client = jmapc.Client.create_with_password(
       host="jmap.example.com",
       user="your_username",
       password="your_password"
   )

This method uses HTTP Basic Authentication and is useful when you have username/password credentials instead of an API token.

Getting Identities
------------------

Identities represent the email addresses you can send from:

.. code-block:: python

   # Get all identities
   identities = client.request(jmapc.methods.identity.IdentityGet())
   
   for identity in identities.list:
       print(f"Identity {identity.id} is for {identity.name} at {identity.email}")

Working with Mailboxes
----------------------

Mailboxes are containers for emails (like folders):

.. code-block:: python

   # Get all mailboxes
   mailboxes = client.request(jmapc.methods.mailbox.MailboxGet(ids=None))
   
   for mailbox in mailboxes.list:
       print(f"Mailbox: {mailbox.name} ({mailbox.total_emails} emails)")

Querying Emails
---------------

To search for emails, use the Email/query method:

.. code-block:: python

   # Query for emails in the inbox
   email_query = client.request(jmapc.methods.email.EmailQuery(
       filter=jmapc.models.email.EmailQueryFilterCondition(
           in_mailbox="inbox_mailbox_id"
       ),
       limit=10
   ))
   
   # Get the actual email objects
   if email_query.ids:
       emails = client.request(jmapc.methods.email.EmailGet(
           ids=email_query.ids,
           properties=["id", "subject", "from", "receivedAt"]
       ))
       
       for email in emails.list:
           print(f"Subject: {email.subject}")
           print(f"From: {email.from_[0].email}")
           print(f"Received: {email.received_at}")
           print("---")

Combined Requests
-----------------

You can combine multiple requests in a single call for efficiency:

.. code-block:: python

   # Create a list of method calls
   methods = [
       jmapc.methods.identity.IdentityGet(),
       jmapc.methods.mailbox.MailboxGet(ids=None)
   ]
   
   # Execute the combined request
   responses = client.request(methods)
   
   # Access results by index
   identities = responses[0]
   mailboxes = responses[1]

Using Result References
-----------------------

You can reference the results of one method call in another using the Invocation pattern:

.. code-block:: python

   from jmapc.methods import Invocation
   
   # Create invocations with specific IDs
   invocations = [
       Invocation(
           id="emailQuery",
           method=jmapc.methods.email.EmailQuery(
               filter=jmapc.models.email.EmailQueryFilterCondition(
                   in_mailbox="inbox_mailbox_id"
               ),
               limit=5
           )
       ),
       Invocation(
           id="emailGet", 
           method=jmapc.methods.email.EmailGet(
               ids=jmapc.ResultReference(
                   name="Email/query",
                   path="/ids",
                   result_of="emailQuery"
               ),
               properties=["id", "subject", "from"]
           )
       )
   ]
   
   responses = client.request(invocations)
   emails = responses[1].response  # Get the EmailGet response

Error Handling
--------------

The library provides comprehensive error handling:

.. code-block:: python

   try:
       response = client.request(jmapc.methods.email.EmailGet(
           ids=["invalid_id"]
       ), raise_errors=True)
   except jmapc.ClientError as e:
       print(f"Client error: {e}")
       # Access the raw response for debugging
       print(f"Raw response: {e.result}")
   
   # Or handle errors manually without exceptions
   response = client.request(jmapc.methods.email.EmailGet(
       ids=["invalid_id"]
   ), raise_errors=False)
   
   if isinstance(response, jmapc.errors.Error):
       print(f"JMAP error: {response.type}")
   else:
       print("Success!")

Next Steps
----------

* Read the :doc:`authentication` guide for different authentication methods
* Explore the :doc:`examples` for more detailed use cases
* Check the :doc:`api/client` for the complete API reference 