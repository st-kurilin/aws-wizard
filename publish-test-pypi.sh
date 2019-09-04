#!/usr/bin/env bash

VERSION="0.0.14"
sed -i '' "s|version='0.0..'|version='${VERSION}'|g" ./src/setup.py
python3 ./src/setup.py sdist
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ "dist/awswizard-${VERSION}.tar.gz"
echo "......................"
echo "......................"
echo "pip install --index-url https://test.pypi.org/simple/ awswizard==${VERSION}"
