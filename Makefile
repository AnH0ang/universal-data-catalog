ENVNAME := .venv
VENV := $(ENVNAME)/bin
PYTHON = $(VENV)/python

.PHONY: test
test:
	$(VENV)/pytest

.PHONY: clean
clean:
	rm -rf dist
	rm -f .coverage
	rm -f coverage.xml
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf *.egg-info

.PHONY: install
install:
	poetry install -E all

.PHONY: lint
lint:
	pre-commit run --all-files
