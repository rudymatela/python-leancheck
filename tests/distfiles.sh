#!/bin/bash
#
# Tests python-leancheck's source distribution
#
# * checks compatibility with case-insensitive file systems
# * checks that all git tracked files are included
#
# Using setuptools-scm would automatically achieve the second item,
# but we do not want to impose a dependency just for this.
# Plus its nice to have a MANIFEST.in with an explicit list of extras...
#
# 2026 Rudy Matela

set -xe

export LC_ALL=C  # consistent sort:w

pkgbase=`poetry version | sed -e 's/ /-/'`
tarball=dist/$pkgbase.tar.gz

# [ -f $tarball ] ||  # uncomment for troubleshooting this file
make sdist

mkdir -p tmp

tar -tf $tarball | sort   > tmp/ls-tar
sort --ignore-case          tmp/ls-tar > tmp/ls-tar-i
sort --ignore-case --unique tmp/ls-tar > tmp/ls-tar-iu
diff -rud tmp/ls-tar-i tmp/ls-tar-iu

if [ -d .git ] && git --version && git ls-files >tmp/ls-git
then
	sort tmp/ls-git >tmp/ls-git-sorted

	sed s,$pkgbase/,, tmp/ls-tar |
	grep -v "/$" |
	grep -v "^setup.cfg$" |
	grep -v "\.egg-info/" |
	grep -v "^PKG-INFO$" |
	grep -v "^$" >tmp/ls-tar-f

	diff -rud tmp/ls-git-sorted tmp/ls-tar-f
fi

rm -r tmp/ls-tar* tmp/ls-git*
