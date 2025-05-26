jmapc: A JMAP client library for Python
========================================

.. image:: https://img.shields.io/pypi/v/jmapc
   :target: https://pypi.org/project/jmapc/
   :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/jmapc
   :target: https://pypi.org/project/jmapc/
   :alt: PyPI - Python Version

.. image:: https://img.shields.io/github/checks-status/smkent/jmapc/main?label=build
   :target: https://github.com/smkent/jmapc/actions?query=branch%3Amain
   :alt: Build

.. image:: https://codecov.io/gh/smkent/jmapc/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/smkent/jmapc
   :alt: codecov

**jmapc** is a Python client library for the `JMAP protocol <https://jmap.io>`_.
JMAP (JSON Meta Application Protocol) is a modern, efficient protocol for 
synchronizing email, calendars, and contacts.

Features
--------

Currently implemented:

* Basic models for JMAP objects
* Request methods:

  * ``Core/echo``
  * ``Email/changes``, ``Email/copy``, ``Email/get``, ``Email/query``, ``Email/queryChanges``, ``Email/set``
  * ``EmailSubmission/*`` (``get``, ``changes``, ``query``, ``queryChanges``, ``set``)
  * ``Identity/*`` (``get``, ``changes``, ``set``)
  * ``Mailbox/*`` (``get``, ``changes``, ``query``, ``queryChanges``, ``set``)
  * ``SearchSnippet/*`` (``get``)
  * ``Thread/*`` (``get``, ``changes``)
  * Arbitrary methods via the ``CustomMethod`` class

* Fastmail-specific methods:

  * ``MaskedEmail/*`` (``get``, ``set``)

* Combined requests with support for result references
* Basic JMAP method response error handling
* EventSource event handling
* Unit tests for basic functionality and methods

Installation
------------

jmapc is available on PyPI and can be installed with pip:

.. code-block:: console

   pip install jmapc

Quick Start
-----------

Here's a simple example to get you started:

.. code-block:: python

   import jmapc

   # Create a client with your JMAP server details
   client = jmapc.Client.create_with_api_token(
       host="jmap.example.com",
       api_token="your_api_token_here"
   )

   # Get identities
   identities = client.request(jmapc.methods.identity.IdentityGet())
   for identity in identities.list:
       print(f"Identity {identity.id} {identity.email}")

Documentation Contents
======================

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   authentication
   examples
   
.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/client
   api/methods
   api/models

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 