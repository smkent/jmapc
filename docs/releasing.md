---
title: Releasing a new version
icon: lucide/rocket
---

# Releasing a new version

Release version numbers should follow [Semantic Versioning][semver].

To create a release, run `mise run release` with one of `patch`, `minor`, or
`major` corresponding to the version number component to update:

```sh
mise run release patch|minor|major
```

A new tag with the new release version number will be created automatically
using [bump-my-version][bump-my-version] (for example, `v1.2.3`).

Afterward, push the new release tag:

```sh
git push --tags
```

* A corresponding [GitHub release][github-releases]
  will be created automatically.

    [![GitHub Release][github-release-badge]][github-release-latest]

* A release package will be built and [uploaded to PyPI][pypi-project].

    [![PyPI][pypi-badge]][pypi-project]

[bump-my-version]: https://callowayproject.github.io/bump-my-version/
[github-release-badge]: https://img.shields.io/github/v/release/smkent/jmapc
[github-release-latest]: https://github.com/smkent/jmapc/releases/latest
[github-releases]: https://github.com/smkent/jmapc/releases
[pypi-badge]: https://img.shields.io/pypi/v/jmapc
[pypi-project]: https://pypi.org/project/jmapc/
[semver]: https://semver.org/
