# jmapc

A [JMAP][jmapio] client library for Python

## Examples

First, run `poetry install` to set up your local repository.

[Any of the examples](/examples) can be invoked with `poetry run`:

```sh
JMAP_HOST=jmap.example.com \
JMAP_USER=ness \
JMAP_PASSWORD=pk_fire \
poetry run examples/core.py
```

If successful, `examples/core.py` should output:

```
CoreEchoResponse(data={'hello': 'world'})
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
