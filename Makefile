PYTHON_VERSION = python3.8
VIRTUALENV := .venv

virtualenv:
	@if [ -d $(VIRTUALENV) ]; then rm -rf $(VIRTUALENV); fi
	@mkdir -p $(VIRTUALENV)
	virtualenv --python $(PYTHON_VERSION) $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip3 install -r requirements_dev.txt
	${VIRTUALENV}/bin/pre-commit install
	source ${VIRTUALENV}/bin/activate && pip3 install --editable .


update-requirements-txt: VIRTUALENV := /tmp/update-requirements-virtualenv
update-requirements-txt:
	@if [ -d $(VIRTUALENV) ]; then rm -rf $(VIRTUALENV); fi
	@mkdir -p $(VIRTUALENV)
	virtualenv --python $(PYTHON_VERSION) $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip3 install -r unpinned_requirements.txt
	echo "# Created by 'make update-requirements-txt'. DO NOT EDIT!" > requirements.txt
	$(VIRTUALENV)/bin/pip freeze | grep -v pkg-resources==0.0.0 >> requirements.txt


reqs:
	pip3 install -r requirements_dev.txt


dist:
	rm -rf dist
	python -m pip install --upgrade build
	python -m build


changelog:
	@gitchangelog > CHANGELOG.rst


clean:
	rm -rf dist src/nervaluate.egg-info .tox .coverage .mypy_cache .pytest_cache


test:
	PYTHONPATH=src coverage run --rcfile=setup.cfg --source=src -m pytest
	PYTHONPATH=src coverage report --rcfile=setup.cfg


lint:
	black -t py38 -l 120 src tests
	pylint --rcfile=pylint.cfg src tests
	flake8 --config=setup.cfg src tests


typing:
	mypy --config setup.cfg src


pre-commit-all:
	pre-commit run --all-files


all:
	make clean
	make lint
	make typing
	make test