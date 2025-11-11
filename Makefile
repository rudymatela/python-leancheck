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


release:
	@echo '1. Bump version in pyproject.toml to even patch (02468)'
	@echo '2. make upload-test'
	@echo '3. Look at https://test.pypi.org/project/leancheck/'
	@echo '4. Commit and tag'
	@echo '5. make upload-for-real-this-time'
	@echo '6. Rinse & repeat'

# Generates a distribution archive for PyPI
#
# See: https://packaging.python.org/en/latest/tutorials/packaging-projects/
#
# Needed: python-setuptools; twine
.PHONY: dist
dist:
	python -m build

upload-test: dist
	python3 -m twine upload --repository testpypi dist/*

upload-for-real-this-time: dist
	echo 'Uploading for real in PyPI in 6 seconds (Ctrl-C to abort)'
	sleep 6
	python3 -m twine upload dist/*

# alias to dist
sdist: dist


%.run: %.py
	PYTHONPATH=src python $<

%.repl: %.py
	PYTHONPATH=src python -i $<
