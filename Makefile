# Makefile for python-leancheck
#
# (C) 2023-2024  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)

all:
	python src/leancheck.py

repl:
	python -i src/leancheck.py -c 'from leancheck import *'

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
	rm -rf __pycache__ src/__pycache__ tests/__pycache__ .pytest_cache

%.run: %.py
	PYTHONPATH=src python $<

%.repl: %.py
	PYTHONPATH=src python -i $<
