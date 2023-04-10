PYTHON_VERSION = python3.8
VIRTUALENV := .venv

.PHONY: virtualenv
virtualenv:
	@if [ -d $(VIRTUALENV) ]; then rm -rf $(VIRTUALENV); fi
	@mkdir -p $(VIRTUALENV)
	virtualenv --python $(PYTHON_VERSION) $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip3 install -r requirements_dev.txt
	$(VIRTUALENV)/bin/python setup.py develop --no-deps
	${VIRTUALENV}/bin/pre-commit install

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
	rm -rf dist src/nervaluate.egg-info .tox .coverage coverage.xml .mypy_cache

.PHONY: changelog
changelog:
	@gitchangelog > CHANGELOG.rst

.PHONY: test
test:
	tox

.PHONY: lint
lint:
	black --check -t py38 -l 120 .
	pylint src tests --rcfile=pylint.cfg
	flake8 src tests --config=setup.cfg

.PHONY: mypy
mypy:
	mypy --config setup.cfg src
