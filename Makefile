dist:
	-rm -r dist
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