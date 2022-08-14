# jmapc: A [JMAP][jmapio] client library for Python

[![PyPI](https://img.shields.io/pypi/v/jmapc)][pypi]
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jmapc)][pypi]
[![Build](https://img.shields.io/github/checks-status/smkent/jmapc/master?label=build)][gh-actions]
[![codecov](https://codecov.io/gh/smkent/jmapc/branch/master/graph/badge.svg)][codecov]
[![GitHub stars](https://img.shields.io/github/stars/smkent/jmapc?style=social)][repo]

[![jmapc][logo]](#)

jmapc is in initial development.

Currently implemented:

* Basic models
* Request methods:
  * `Core/echo`
  * `Email/changes`
  * `Email/copy`
  * `Email/get`
  * `Email/query`
  * `Email/queryChanges`
  * `Email/set`
  * `EmailSubmission/*` (`get`, `changes`, `query`, `queryChanges`, `set`)
  * `Identity/*` (`get`, `changes`, `set`)
  * `Mailbox/*` (`get`, `changes`, `query`, `queryChanges`, `set`)
  * `Thread/*` (`get`, `changes`)
  * Arbitrary methods via the `CustomMethod` class
* Combined requests with support for result references
* Basic JMAP method response error handling
* EventSource event handling
* Unit tests for basic functionality and methods

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
JMAP_API_TOKEN=ness__pk_fire \
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

[codecov]: https://codecov.io/gh/smkent/jmapc
[cookie-python]: https://github.com/smkent/cookie-python
[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[gh-actions]: https://github.com/smkent/jmapc/actions?query=branch%3Amaster
[logo]: https://raw.github.com/smkent/jmapc/master/docs/logo.png
[jmapc-pypi]: https://pypi.org/project/jmapc/
[jmapio]: https://jmap.io
[poetry]: https://python-poetry.org/docs/#installation
[pypi]: https://pypi.org/project/jmapc/
[repo]: https://github.com/smkent/jmapc
