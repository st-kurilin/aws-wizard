#!/usr/bin/env bash

pip install -e ./src/
echo ".................."
python3 -m awswizard "$@"
