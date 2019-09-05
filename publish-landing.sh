#!/usr/bin/env bash

(cd ./landing; npm run pack)
echo "~~~~~"
./run.sh update_static aws-wizard.com -d ./landing/out
echo "~~~~~"
