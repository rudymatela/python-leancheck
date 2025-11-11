python-leancheck release instructions
=====================================

1. Upload on test-PyPI

	$ make upload-test

2. Look at https://test.pypi.org/project/leancheck/

3. Test install with:

	$ make test-install

4. Bump version in `pyproject.toml` to even patch (02468)

5. Commit and tag

	$ git commit
	$ git tag -a vX.Y.Z

6. Upload for real on PyPI:

	$ make upload-for-real-this-time

7. Bump version in `pyproject.toml` to odd "dev" patch (13579)

8. Commit

9. Rinse & repeat.
