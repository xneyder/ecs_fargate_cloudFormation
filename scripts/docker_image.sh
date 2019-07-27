#!/bin/bash
#Script to build the docker image and push it to ECR

if [ $# -lt 1 ]
then
        echo "Usage `basename $0` <ECR URL>"
        echo "Example `basename $0` 712171867.dkr.ecr.us-east-1.amazonaws.com/helloworld"
        exit 1
fi

APP_DIR="../"
#Remove spaces
ECR_URL=`echo $1 | sed "s/ //g"`
#Get the Tag from the ecrUrl 
DOCKER_TAG=`echo ${ECR_URL} | cut -f2 -d'/'`

cd $APP_DIR
#build the image
docker build -t ${DOCKER_TAG}:latest .
#tag the image
docker tag ${DOCKER_TAG} ${ECR_URL}:latest
#Login to ecr
aws ecr get-login --no-include-email | sh
#Push the image to ecr
docker push ${ECR_URL}

