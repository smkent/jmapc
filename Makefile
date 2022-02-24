PIPENV=./pipenv
BLACK_ARGS=-l 79
SOURCE_DIRS=tests/ jmapc/

.PHONY: all
all: rm sync

.PHONY: testall
testall: all test

.PHONY: rm
rm:
	-$(PIPENV) --rm

.PHONY: sync
sync:
	$(PIPENV) sync --dev
	$(PIPENV) run python setup.py develop --script-dir=bin/

.PHONY: dev
update:
	$(PIPENV) update --dev
	$(PIPENV) run pipenv-setup sync --pipfile

.PHONY: my
my:
	$(PIPENV) run mypy

.PHONY: test
test:
	$(PIPENV) run flake8 -- .
	$(PIPENV) run isort --quiet --check-only -- $(SOURCE_DIRS)
	$(PIPENV) run black $(BLACK_ARGS) -q --check --diff --color -- $(SOURCE_DIRS)
	$(PIPENV) run mypy
	$(PIPENV) run pytest

.PHONY: lint
lint:
	$(PIPENV) run isort -- $(SOURCE_DIRS)
	$(PIPENV) run black $(BLACK_ARGS) -- $(SOURCE_DIRS)
