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
	pytest
	validate-pyproject pyproject.toml

.PHONY: examples
examples:
	PYTHONPATH=src python examples/arith.py
	PYTHONPATH=src python examples/sort.py

clean:
	rm -rf __pycache__ src/__pycache__ tests/__pycache__ .pytest_cache
