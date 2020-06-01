#!/bin/bash

set -e 

sudo chown :808 ./shared-data \
    && chmod 775 ./shared-data \
    && chmod g+s ./shared-data

docker image build \
    --build-arg BUILD_DATE=$(date +%Y-%m-%d_%H:%M:%S) \
    -t ryantanaka/pegasus5-condor .



