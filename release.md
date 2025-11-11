python-leancheck release instructions
=====================================

1. Bump version in `pyproject.toml` to even patch (02468)

2. Upload on test-PyPI

	$ make upload-test

3. Look at https://test.pypi.org/project/leancheck/

4. Test install with:

	$ make test-install

5. Commit and tag

	$ git commit
	$ git tag -a vX.Y.Z

6. Upload for real on PyPI:

	$ make upload-for-real-this-time

7. Rinse & repeat.
