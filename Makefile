PYTHON_VERSION = python3.8
VIRTUALENV := .venv

.PHONY: virtualenv
virtualenv:
	@if [ -d $(VIRTUALENV) ]; then rm -rf $(VIRTUALENV); fi
	@mkdir -p $(VIRTUALENV)
	virtualenv --python $(PYTHON_VERSION) $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip3 install -r requirements_dev.txt
	${VIRTUALENV}/bin/pre-commit install
	source ${VIRTUALENV}/bin/activate && pip3 install --editable .

.PHONY: update-requirements-txt
update-requirements-txt: VIRTUALENV := /tmp/update-requirements-virtualenv
update-requirements-txt:
	@if [ -d $(VIRTUALENV) ]; then rm -rf $(VIRTUALENV); fi
	@mkdir -p $(VIRTUALENV)
	virtualenv --python $(PYTHON_VERSION) $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip3 install -r unpinned_requirements.txt
	echo "# Created by 'make update-requirements-txt'. DO NOT EDIT!" > requirements.txt
	$(VIRTUALENV)/bin/pip freeze | grep -v pkg-resources==0.0.0 >> requirements.txt

.PHONY: reqs
reqs:
	pip3 install -r requirements_dev.txt

.PHONY: dist
dist:
	-rm -r dist
	python -m pip install --upgrade build
	python -m build

pypi_upload: dist
	python -m twine upload dist/*

clean:
	rm -rf dist src/nervaluate.egg-info .tox .coverage coverage.xml .mypy_cache .pytest_cache

clean_venv:
	rm -rf .venv

.PHONY: changelog
changelog:
	@gitchangelog > CHANGELOG.rst


# code quality related measures

.PHONY: test
test:
	tox

.PHONY: lint
lint:
	black --check -t py38 -l 120 src tests
	pylint --rcfile=pylint.cfg src tests
	flake8 --config=setup.cfg src tests

.PHONY: mypy
mypy:
	mypy --config setup.cfg src

pre-commit-all:
	pre-commit run --all-files