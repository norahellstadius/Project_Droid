#!/bin/bash

# Define environment variables
export IMAGE_NAME="app:1.0"

#Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .

