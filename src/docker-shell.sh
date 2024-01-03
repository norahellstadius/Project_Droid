#!/bin/bash

# Define some environment variables
export IMAGE_NAME="app:2.0"

#Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .

