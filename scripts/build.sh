#!/usr/bin/env bash
## Description:
##  Script to build the docker image.
##
## Usage: ./build.sh ARG1 ARG2
##
## Arguments:
##  ARG1        Docker image name (defaults to 'dextra/big-data-python').
##  ARG2        Docker image version (defaults to 'latest').

IMG_NAME_DEFAULT=dextra/big-data-python
IMG_NAME=${1:-$IMG_NAME_DEFAULT}

IMG_VERSION_DEFAULT=latest
IMG_VERSION=${2:-$IMG_VERSION_DEFAULT}

echo "Building [${IMG_NAME}]..."

docker build -t ${IMG_NAME}:${IMG_VERSION} \
    .