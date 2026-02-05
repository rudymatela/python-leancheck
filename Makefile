# Makefile for python-leancheck
#
# (C) 2023-2025  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)

# Sets the number of jobs to the the number of processors minus one.
NJOBS := $(shell grep ^processor /proc/cpuinfo | head -n -1 | wc -l | sed 's/^0$$/1/')

all: run

repl:
	PYTHONPATH=src python -ic 'import leancheck; from leancheck import *; from leancheck.iitertools import *'

test: run pytest mypy diff-test

pytest:
	pytest

mypy:
	mypy src/ tests/ examples/

black:
	black -l99 src/ tests/ examples/

validate-pyproject:
	validate-pyproject pyproject.toml

doc:
	PYTHONPATH=src pdoc leancheck -o docs

opendoc: doc
	wbi docs/index.html

run:       $(patsubst %.py,%.run, $(wildcard src/leancheck/*.py))

.PHONY: examples
examples:  $(patsubst %.py,%.run, $(wildcard examples/*.py))

txt:       $(patsubst %.py,%.txt, $(wildcard examples/*.py))

diff-test: $(patsubst %.py,%.diff,$(wildcard examples/*.py))

clean:
	rm -rf __pycache__ src/__pycache__ tests/__pycache__ .pytest_cache .mypy_cache
	rm -rf docs/ dist/ tmp/ src/leancheck.egg-info

fastest:
	make test -j$(NJOBS)


release:
	cat release.md

# Generates a distribution archive for PyPI
#
# See: https://packaging.python.org/en/latest/tutorials/packaging-projects/
#
# Needed: python-setuptools; twine
.PHONY: dist
dist:
	python -m build

upload-test: dist
	twine upload --skip-existing --repository testpypi dist/*

test-install:
	rm -rf tmp/test-install
	mkdir -p tmp/test-install
	python -m venv tmp/test-install
	source tmp/test-install/bin/activate && \
	pip install --index-url https://test.pypi.org/simple/ --no-deps leancheck && \
	python -ic 'from leancheck import *; print("run check(lambda x: x + x > x, types = [int])")'


upload-for-real-this-time: dist
	echo 'Uploading for real in PyPI in 6 seconds (Ctrl-C to abort)'
	sleep 6
	twine upload --skip-existing dist/*

# alias to dist
sdist: dist

clone-docs:
	rm -r docs
	git clone git@github.com:leancheck/leancheck.github.io.git docs


%.run: %.py
	PYTHONPATH=src python $<

%.repl: %.py
	PYTHONPATH=src python -i $<

%.txt: %.py
	PYTHONPATH=src python $< >$@

%.diff: %.py
	PYTHONPATH=src python $< | diff -rud $*.txt -
