#!/usr/bin/env bash

(cd ./landing; npm run pack)
echo "~~~~~"
./run.sh update-static-website aws-wizard.com -d ./landing/out
echo "~~~~~"
