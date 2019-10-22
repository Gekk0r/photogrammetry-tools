#!/bin/bash

TAG="latest"
TAG=$(git rev-parse --short HEAD)

docker build -t geki/photogrammetry-tools:latest -t geki/photogrammetry-tools:$TAG . && \
  docker push geki/photogrammetry-tools:$TAG && \
  docker push geki/photogrammetry-tools:latest
  