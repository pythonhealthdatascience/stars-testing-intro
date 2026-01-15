pylint . --ignore-paths=^pages/code/.*$ --disable=duplicate-code
flake8 . --exclude pages/code

lintquarto -l pylint -p .
lintquarto -l flake8 -p .