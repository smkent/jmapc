Installation
============

Requirements
------------

jmapc requires Python 3.9 or later.

Installing from PyPI
---------------------

The easiest way to install jmapc is from PyPI using pip:

.. code-block:: console

   pip install jmapc

This will install jmapc and all its required dependencies.

Installing from Source
----------------------

If you want to install from source (for development or to get the latest unreleased features):

.. code-block:: console

   git clone https://github.com/smkent/jmapc.git
   cd jmapc
   pip install .

Development Installation
------------------------

For development, it's recommended to use Poetry:

.. code-block:: console

   git clone https://github.com/smkent/jmapc.git
   cd jmapc
   poetry install

This will install jmapc in development mode along with all development dependencies.

Verification
------------

To verify that the installation was successful, you can run:

.. code-block:: python

   import jmapc
   print(jmapc.__version__)

This should print the version number of jmapc without any errors. 