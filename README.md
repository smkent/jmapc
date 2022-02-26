# jmapc: A [JMAP][jmapio] client library for Python

jmapc is in initial development.

Currently implemented:

* Basic models
* Request methods:
  * `Core/echo`
  * `Email/get`
  * `Email/query`
  * `Identity/get`
  * `Thread/get`
  * `Mailbox/get`
  * `Mailbox/query`
* Combined requests with support for result references
* Basic JMAP method response error handling
* Unit tests for basic functionality and methods

Todo list:

* Implement `EmailSubmission` methods for sending email
* Write documentation

## Examples

First, run `poetry install` to set up your local repository.

[Any of the examples](/examples) can be invoked with `poetry run`:

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

## Development

Prerequisites: [Poetry][poetry]

* Setup: `poetry install`
* Run all tests: `poetry run poe test`
* Fix linting errors: `poetry run poe lint`

---

Created from [smkent/cookie-python][cookie-python] using
[cookiecutter][cookiecutter]

[cookie-python]: https://github.com/smkent/cookie-python
[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[jmapio]: https://jmap.io
[poetry]: https://python-poetry.org/docs/#installation
