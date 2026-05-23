# jmapc

A [JMAP][jmapio] client library for Python

[![License](https://img.shields.io/github/license/smkent/jmapc)](https://github.com/smkent/jmapc/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/jmapc)](https://pypi.org/project/jmapc/)
[![Python](https://img.shields.io/pypi/pyversions/jmapc)](https://pypi.org/project/jmapc/)
[![CI](https://github.com/smkent/jmapc/actions/workflows/ci.yaml/badge.svg)](https://github.com/smkent/jmapc/actions/workflows/ci.yaml)
[![Coverage](https://codecov.io/gh/smkent/jmapc/branch/main/graph/badge.svg)](https://codecov.io/gh/smkent/jmapc)
[![Renovate](https://img.shields.io/badge/renovate-enabled-brightgreen?logo=renovatebot)](https://renovatebot.com)
[![GitHub stars](https://img.shields.io/github/stars/smkent/jmapc?style=social)](https://github.com/smkent/jmapc)

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
  * `SearchSnippet/*` (`get`)
  * `Thread/*` (`get`, `changes`)
  * Arbitrary methods via the `CustomMethod` class
* Fastmail-specific methods:
  * [`MaskedEmail/*` (`get`, `set`)][fastmail-maskedemail]
* Combined requests with support for result references
* Basic JMAP method response error handling
* EventSource event handling
* Unit tests for basic functionality and methods

## Installation

Install in any environment where `pip` is available:

```sh
pip install jmapc
```

### Installation in projects

Install in a project, such as with [`uv`][uv] or [`poetry`][poetry]:

```sh
uv add jmapc
```

```sh
poetry add jmapc
```

## Examples

Any of the included examples can be invoked with `uv run`:

```sh
JMAP_HOST=jmap.example.com \
JMAP_API_TOKEN=ness__pk_fire \
uv run examples/identity_get.py
```

If successful, `examples/identity_get.py` should output something like:

```
Identity 12345 is for Ness at ness@onett.example.com
Identity 67890 is for Ness at ness-alternate@onett.example.com
```

## Project template

This project is generated and maintained with [copier-python][copier-python].

[codecov]: https://codecov.io/gh/smkent/jmapc
[copier-python]: https://smkent.github.io/copier-python
[fastmail-maskedemail]: https://www.fastmail.com/developer/maskedemail/
[jmapio]: https://jmap.io
[logo]: https://raw.github.com/smkent/jmapc/main/img/jmapc.png
[pipx]: https://pypa.github.io/pipx/
[poetry]: https://python-poetry.org/
[uv]: https://docs.astral.sh/uv/
