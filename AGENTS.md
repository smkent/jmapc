# Environment/Tools

* `mise` manages dev tools and tasks, including `uv` which manages Python and dependencies.
* Use `uv add`/`uv run python` instead of bare `pip`/`python`
* `mise install`: After-clone setup (install tools, dependencies, pre-commit hooks)
* `mise run lint`: Pre-commit hooks (via `pre-commit`-compatible `prek`) including lint, format, type check (ruff, ty)
* `mise run test`: Run tests (accepts pytest arguments)
* `mise run lt`: Lint+test (no arguments)
* `mise run snapup`: Update test snapshots (syrupy, accepts pytest arguments)
