#!/bin/bash

sls deploy --verbose --aws-profile $1

if [ $? -ne 0 ]; then
  echo "Error: Error while deploying the project"

else
  echo "Deploying labdas image..."
  aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 887408025590.dkr.ecr.us-east-1.amazonaws.com
  
  echo "Deploying raw-to-staged..."
  cd raw_to_staged
  docker build -t test-raw .
  docker tag test-raw:latest 887408025590.dkr.ecr.us-east-1.amazonaws.com/test-raw:latest
  docker push 887408025590.dkr.ecr.us-east-1.amazonaws.com/test-raw:latest
  cd ..
  
  echo "Deploying staged-to-consume..."
  cd staged_to_consumed
  docker build -t test-staged .
  docker tag test-staged:latest 887408025590.dkr.ecr.us-east-1.amazonaws.com/test-staged:latest
  docker push 887408025590.dkr.ecr.us-east-1.amazonaws.com/test-staged:latest

fi