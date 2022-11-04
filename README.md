# jmapc: A [JMAP][jmapio] client library for Python

[![PyPI](https://img.shields.io/pypi/v/jmapc)][pypi]
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jmapc)][pypi]
[![Build](https://img.shields.io/github/checks-status/smkent/jmapc/main?label=build)][gh-actions]
[![codecov](https://codecov.io/gh/smkent/jmapc/branch/main/graph/badge.svg)][codecov]
[![GitHub stars](https://img.shields.io/github/stars/smkent/jmapc?style=social)][repo]

[![jmapc][logo]](#)

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
* Fastmail-specific methods:
  * [`MaskedEmail/*` (`get`, `set`)][fastmail-maskedemail]
* Combined requests with support for result references
* Basic JMAP method response error handling
* EventSource event handling
* Unit tests for basic functionality and methods

## Installation

[jmapc is available on PyPI][pypi]:

```
pip install jmapc
```

## Examples

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

## Development

### [Poetry][poetry] installation

Via [`pipx`][pipx]:

```console
pip install pipx
pipx install poetry
pipx inject poetry poetry-dynamic-versioning poetry-pre-commit-plugin
```

Via `pip`:

```console
pip install poetry
poetry self add poetry-dynamic-versioning poetry-pre-commit-plugin
```

### Development tasks

* Setup: `poetry install`
* Run static checks: `poetry run poe lint` or
  `poetry run pre-commit run --all-files`
* Run static checks and tests: `poetry run poe test`

---

Created from [smkent/cookie-python][cookie-python] using
[cookiecutter][cookiecutter]

[codecov]: https://codecov.io/gh/smkent/jmapc
[cookie-python]: https://github.com/smkent/cookie-python
[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[fastmail-maskedemail]: https://www.fastmail.com/developer/maskedemail/
[gh-actions]: https://github.com/smkent/jmapc/actions?query=branch%3Amain
[logo]: https://raw.github.com/smkent/jmapc/main/img/jmapc.png
[jmapio]: https://jmap.io
[pipx]: https://pypa.github.io/pipx/
[poetry]: https://python-poetry.org/docs/#installation
[pypi]: https://pypi.org/project/jmapc/
[repo]: https://github.com/smkent/jmapc
