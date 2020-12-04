#!/bin/bash

docker container run \
    --shm-size=1024m \
    -p 8888:8888 \
    -p 5000:5000 \
    --privileged \
    --mount type=bind,source="$(pwd)"/shared-data,target=/home/scitech/shared-data \
    --rm \ 
    ryantanaka/pegasus5-condor
