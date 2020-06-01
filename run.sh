#!/bin/bash

docker container run \
    -p 8888:8888 \
    --privileged \
    --mount type=bind,source="$(pwd)"/shared-data,target=/home/scitech/shared-data \
    ryantanaka/pegasus5-condor
