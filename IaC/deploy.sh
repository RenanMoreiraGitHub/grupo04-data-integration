#!/bin/bash

sls deploy --verbose --aws-profile $1

if [ $? -ne 0 ]; then
  echo "Error: Error while deploying the project"

else
  echo "Deploying labdas image..."
  aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 181076026206.dkr.ecr.us-east-1.amazonaws.com
  
  echo "Deploying raw-to-staged..."
  cd raw_to_staged
  docker build -t soybean-raw .
  docker tag soybean-raw:latest 181076026206.dkr.ecr.us-east-1.amazonaws.com/soybean-raw:latest
  docker push 181076026206.dkr.ecr.us-east-1.amazonaws.com/soybean-raw:latest
  cd ..
  
  echo "Deploying staged-to-consume..."
  cd staged_to_consumed
  docker build -t soybean-staged .
  docker tag soybean-staged:latest 181076026206.dkr.ecr.us-east-1.amazonaws.com/soybean-staged:latest
  docker push 181076026206.dkr.ecr.us-east-1.amazonaws.com/soybean-staged:latest

fi