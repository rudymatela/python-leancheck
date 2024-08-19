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

.PHONY: examples
examples: \
	examples/arith.run \
	examples/sort.run \
	examples/bool.run

clean:
	rm -rf __pycache__ src/__pycache__ tests/__pycache__ .pytest_cache

%.run: %.py
	PYTHONPATH=src python $<

%.repl: %.py
	PYTHONPATH=src python -i $<
