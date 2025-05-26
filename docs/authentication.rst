Authentication
==============

jmapc supports multiple authentication methods for connecting to JMAP servers.
The authentication method you use depends on your JMAP server configuration.

API Token Authentication
------------------------

The most common and recommended authentication method is using an API token.
Many JMAP providers (like Fastmail) provide API tokens for programmatic access.

.. code-block:: python

   import jmapc

   client = jmapc.Client.create_with_api_token(
       host="jmap.example.com",
       api_token="your_api_token_here"
   )

API tokens are preferred because they:

* Don't require storing passwords in your code
* Can be easily revoked if compromised
* Often have specific scopes/permissions
* Are designed for programmatic access

Basic Authentication
--------------------

You can also use username/password authentication:

.. code-block:: python

   import jmapc

   client = jmapc.Client.create_with_password(
       host="jmap.example.com",
       user="your_username",
       password="your_password"
   )

.. warning::
   
   Using passwords directly in code is not recommended for production applications.
   Consider using environment variables or secure credential storage.

Custom Authentication
---------------------

For more advanced authentication schemes, you can provide a custom authentication object:

.. code-block:: python

   import jmapc
   import requests.auth

   # Custom authentication
   custom_auth = requests.auth.HTTPDigestAuth("username", "password")
   
   client = jmapc.Client(
       host="jmap.example.com",
       auth=custom_auth
   )

Environment Variables
---------------------

For security, it's recommended to store credentials in environment variables:

.. code-block:: python

   import os
   import jmapc

   client = jmapc.Client.create_with_api_token(
       host=os.environ["JMAP_HOST"],
       api_token=os.environ["JMAP_API_TOKEN"]
   )

You can set these environment variables in your shell:

.. code-block:: console

   export JMAP_HOST="jmap.example.com"
   export JMAP_API_TOKEN="your_api_token_here"

Getting API Tokens
-------------------

The process for obtaining API tokens varies by provider:

Fastmail
~~~~~~~~

1. Log in to your Fastmail account
2. Go to Settings → Privacy & Security → Manage API Tokens
3. Create a new API token with the required permissions
4. Use the generated token in your application

Other Providers
---------------

Check your JMAP provider's documentation for instructions on generating API tokens.
Most providers will have them in their account security or developer settings.

Session Management
------------------

jmapc automatically handles JMAP session discovery and management. When you create
a client, it will:

1. Discover the JMAP endpoints using the well-known URL
2. Establish a session with the server
3. Cache session information for efficiency

The session includes important information like:

* Available capabilities
* Account IDs
* Upload/download URLs
* EventSource URLs

You can access session information if needed:

.. code-block:: python

   # Get session information
   session = client.jmap_session
   print(f"Session state: {session.state}")
   print(f"Account ID: {client.account_id}")

Error Handling
--------------

Always handle authentication errors gracefully:

.. code-block:: python

   import jmapc
   from requests.exceptions import HTTPError

   try:
       client = jmapc.Client.create_with_api_token(
           host="jmap.example.com",
           api_token="invalid_token"
       )
       # This will trigger the session request
       session = client.jmap_session
   except HTTPError as e:
       if e.response.status_code == 401:
           print("Authentication failed: Invalid credentials")
       else:
           print(f"HTTP error: {e}")
   except Exception as e:
       print(f"Unexpected error: {e}")

Next Steps
----------

* Learn about making requests in the :doc:`quickstart` guide
* Explore practical usage in the :doc:`examples` section
* Check the :doc:`api/client` for complete API reference 