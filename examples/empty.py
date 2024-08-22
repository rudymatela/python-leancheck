#!/bin/bash
#
# Example: using LeanCHeck to test an empty file

import leancheck

# tests should pass, but leancheck should issue a warning
# that no properties were found.
leancheck.main()
