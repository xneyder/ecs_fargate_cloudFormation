#!/bin/bash
#Script to build the docker image and push it to ECR

APP_DIR="../app/"
ECR_URL="741821171867.dkr.ecr.us-east-1.amazonaws.com/helloworld"
DOCKER_TAG="helloworld"

cd $APP_DIR
#build the image
docker build -t ${DOCKER_TAG}:latest .
#tag the image
docker tag ${DOCKER_TAG} ${ECR_URL}:latest
#Login to ecr
aws ecr get-login --no-include-email | sh
#Push the image to ecr
docker push ${ECR_URL}

