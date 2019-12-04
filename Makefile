
VIRTUALENV := build/virtualenv

$(VIRTUALENV)/.installed:
	@if [ -d $(VIRTUALENV) ]; then rm -rf $(VIRTUALENV); fi
	@mkdir -p $(VIRTUALENV)
	virtualenv --python python3 $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip3 install -r requirements_test.txt
	$(VIRTUALENV)/bin/pip3 install -r requirements_example.txt
	$(VIRTUALENV)/bin/python3 setup.py develop --no-deps
	sudo $(VIRTUALENV)/bin/python3 -m ipykernel install --name nervaluate
	touch $@

.PHONY: virtualenv
virtualenv: $(VIRTUALENV)/.installed

.PHONY: reqs
reqs: 
	pip3 install -r requirements_test.txt
	pip3 install -r requirements_example.txt


.PHONY: test
test: 
	tox

