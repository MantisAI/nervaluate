#################################################################################
# GLOBALS                                                                       #
#################################################################################

PYTHON_VERSION = python3.8
VIRTUALENV := build/virtualenv

#################################################################################
# COMMANDS                                                                      #
#################################################################################

# Set the default location for the virtualenv to be stored
# Create the virtualenv by installing the requirements and test requirements

$(VIRTUALENV)/.installed:
	@if [ -d $(VIRTUALENV) ]; then rm -rf $(VIRTUALENV); fi
	@mkdir -p $(VIRTUALENV)
	virtualenv --python $(PYTHON_VERSION) $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip3 install -r requirements_dev.txt
	$(VIRTUALENV)/bin/python setup.py develop --no-deps
	touch $@

.PHONY: update-requirements-txt
update-requirements-txt: VIRTUALENV := /tmp/update-requirements-virtualenv
update-requirements-txt:
	@if [ -d $(VIRTUALENV) ]; then rm -rf $(VIRTUALENV); fi
	@mkdir -p $(VIRTUALENV)
	virtualenv --python $(PYTHON_VERSION) $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip3 install -r unpinned_requirements.txt
	echo "# Created by 'make update-requirements-txt'. DO NOT EDIT!" > requirements.txt
	$(VIRTUALENV)/bin/pip freeze | grep -v pkg-resources==0.0.0 >> requirements.txt

.PHONY: virtualenv
virtualenv: $(VIRTUALENV)/.installed

.PHONY: reqs
reqs: 
	pip3 install -r requirements_dev.txt

.PHONY: dist
dist:
	-rm -r dist
	python setup.py bdist_wheel

pypi_upload: dist
	python -m twine upload dist/*

.PHONY: changelog
changelog:
	@gitchangelog > CHANGELOG.rst

.PHONY: test
test: 
	tox

