# Environment/Tools

* Python project with `uv`, use `uv add`/`uv run python` instead of bare `pip`/`python`
* `poe setup`: One-time after-clone setup (dependencies, install pre-commit hooks).
* `poe lint`: Pre-commit hooks (via `pre-commit`-compatible `prek`) including lint, format, type check (ruff, ty)
* `poe test`: Run tests (accepts pytest arguments)
* `poe lt`: Lint+test (no arguments)
* `poe snapup`: Update test snapshots (syrupy, accepts pytest arguments)
