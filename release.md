python-leancheck release instructions
=====================================

Releasing `python-leancheck` in 16 easy steps.

0. Make sure to pull from all remotes first

		git pull --all

1. Cleanup dist

		$ rm -r dist/

2. Upload on test-PyPI

		$ make upload-test

3. Look at `https://test.pypi.org/project/leancheck/`

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

9. Publish updated docs:

		$ make pull-docs || make clone-docs
		$ make doc
		$ cd docs
		$ git diff
		$ git commit

10. Bump version in `pyproject.toml` to odd "dev" patch (13579)

11. List latest version in `changelog.md`

12. Commit "dev version bump"

13. Push then push tags

		$ git push && git push --tags

14. Test real install with `pip install leancheck`

15. check documentation at `https://leancheck.github.io`

16. Rinse & repeat.
