# jmapc: A [JMAP][jmapio] client library for Python

![PyPI](https://img.shields.io/pypi/v/jmapc)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jmapc)
[![codecov](https://codecov.io/gh/smkent/jmapc/branch/master/graph/badge.svg)](https://codecov.io/gh/smkent/jmapc)

jmapc is in initial development.

Currently implemented:

* Basic models
* Request methods:
  * `Core/echo`
  * `Email/get`
  * `Email/query`
  * `Email/set`
  * `EmailSubmission/set`
  * `Identity/get`
  * `Mailbox/get`
  * `Mailbox/query`
  * `Thread/get`
  * Arbitrary methods via the `CustomMethod` class
* Combined requests with support for result references
* Basic JMAP method response error handling
* Unit tests for basic functionality and methods

Todo list:

* Write documentation

## Installation

[jmapc is available on PyPI][jmapc-pypi]:

```
pip install jmapc
```

## Development

Prerequisites: [Poetry][poetry]

* Repository setup: `poetry install`
* Run all tests: `poetry run poe test`
* Fix linting errors: `poetry run poe lint`

### Examples

Any of the included examples can be invoked with `poetry run`:

```sh
JMAP_HOST=jmap.example.com \
JMAP_USER=ness \
JMAP_PASSWORD=pk_fire \
poetry run examples/identity_get.py
```

If successful, `examples/identity_get.py` should output something like:

```
Identity 12345 is for Ness at ness@onett.example.com
Identity 67890 is for Ness at ness-alternate@onett.example.com
```

---

Created from [smkent/cookie-python][cookie-python] using
[cookiecutter][cookiecutter]

[cookie-python]: https://github.com/smkent/cookie-python
[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[jmapio]: https://jmap.io
[poetry]: https://python-poetry.org/docs/#installation
[jmapc-pypi]: https://pypi.org/project/jmapc/
