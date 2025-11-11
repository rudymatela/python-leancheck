# Makefile for python-leancheck
#
# (C) 2023-2024  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)

all:
	python src/leancheck.py

repl:
	PYTHONPATH=src python -ic 'from leancheck import *'

test: examples
	python src/leancheck.py
	mypy src/ tests/ examples/
	pytest
	validate-pyproject pyproject.toml

doc:
	PYTHONPATH=src pdoc leancheck -o docs

opendoc: doc
	wbi docs/index.html

.PHONY: examples
examples: \
	examples/arith.run \
	examples/bool.run \
	examples/sort.run \
	examples/empty.run

clean:
	rm -rf __pycache__ src/__pycache__ tests/__pycache__ .pytest_cache .mypy_cache
	rm -rf docs/ dist/ src/leancheck.egg-info


# Generates a distribution archive for PyPI
#
# See: https://packaging.python.org/en/latest/tutorials/packaging-projects/
#
# Needed: python-setuptools; twine
.PHONY: dist
dist:
	python -m build

upload-test:
	python3 -m twine upload --repository testpypi dist/*

# alias to dist
sdist: dist


%.run: %.py
	PYTHONPATH=src python $<

%.repl: %.py
	PYTHONPATH=src python -i $<
