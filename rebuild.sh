rm -rf dist/
pyproject-build
twine upload --verbose --repository pypi dist/*