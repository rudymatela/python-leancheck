python-leancheck release instructions
=====================================

0. Make sure to pull from all remotes first

		git pull --all

1. Cleanup dist

		$ rm -r dist/

2. Upload on test-PyPI

		$ make upload-test

3. Look at https://test.pypi.org/project/leancheck/

4. Test install with:

		$ make test-install

5. Bump version in `pyproject.toml` to even patch (02468)

6. Commit and tag

		$ git commit
		$ git tag -a vX.Y.Z

7. Cleanup dist

		$ rm -r dist/

8. Upload for real on PyPI:

		$ make upload-for-real-this-time

9. Bump version in `pyproject.toml` to odd "dev" patch (13579)

10. Commit "dev version bump"

11. Test real install with `pip install leancheck`

12. Publish updated docs:

		$ make clone-docs # or pull
		$ make docs
		$ cd docs
		$ git diff
		$ git commit

13. Rinse & repeat.
