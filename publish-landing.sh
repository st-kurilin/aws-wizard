#!/usr/bin/env bash

(cd ./landing; npm run pack)
./run.sh -V static_website aws-wizard.com -d ./landing/out
