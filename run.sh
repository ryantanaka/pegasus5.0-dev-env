#!/bin/bash
set -v

#RUNTIME="runc"
RUNTIME="nvidia"

docker container run \
    --shm-size=1024m \
    -p 8888:8888 \
    -p 5000:5000 \
    --runtime $RUNTIME \
    --privileged \
    --mount type=bind,source="$(pwd)"/shared-data,target=/home/scitech/shared-data \
    ryantanaka/pegasus5-condor
