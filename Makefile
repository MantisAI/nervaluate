
VIRTUALENV := build/virtualenv

$(VIRTUALENV)/.installed:
	@if [ -d $(VIRTUALENV) ]; then rm -rf $(VIRTUALENV); fi
	@mkdir -p $(VIRTUALENV)
	virtualenv --python python3 $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip3 install -r requirements_dev.txt
	$(VIRTUALENV)/bin/python3 setup.py develop --no-deps
	touch $@

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

