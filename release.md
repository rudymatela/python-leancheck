python-leancheck release instructions
=====================================

0. Make sure to pull from all remotes first

		git pull --all

1. Upload on test-PyPI

		$ make upload-test

2. Look at https://test.pypi.org/project/leancheck/

3. Test install with:

		$ make test-install

4. Bump version in `pyproject.toml` to even patch (02468)

5. Commit and tag

		$ git commit
		$ git tag -a vX.Y.Z

6. Cleanup dist

		$ rm -r dist/

7. Upload for real on PyPI:

		$ make upload-for-real-this-time

8. Bump version in `pyproject.toml` to odd "dev" patch (13579)

9. Commit "dev version bump"

10. Test real install with `pip install leancheck`

11. Publish updated docs:

		$ make clone-docs # or pull
		$ make docs
		$ cd docs
		$ git diff
		$ git commit

12. Rinse & repeat.
