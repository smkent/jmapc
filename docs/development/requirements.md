---
title: Required software
icon: lucide/bookmark-check
---

# Prerequisites

- [x] A [supported version][python-versions] of [**Python**][python]
- [x] [**git** for verson control][git]
- [x] [Astral's **uv** Python project manager][uv]: `pip install uv` or
  [other supported method][uv-installation]
- [x] [**Copier**][copier]: `uv tool install copier`
- [x] [Poe the Poet][poethepoet] (recommended): `uv tool install poethepoet`

    This provides `poe` without the `uv run` prefix,
    e.g. `poe test` instead of `uv run poe test`

[copier]: https://copier.readthedocs.io
[git]: https://git-scm.com
[poethepoet]: https://poethepoet.natn.io/
[python-versions]: https://devguide.python.org/versions/
[python]: https://python.org
[uv-installation]: https://docs.astral.sh/uv/getting-started/installation/
[uv]: https://docs.astral.sh/uv/
