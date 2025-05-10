#!/bin/bash

# Set variables
ECR_REPO="pictures2stories"
IMAGE_TAG="latest"
IMAGE_NAME="pictures2pages_lambda"
AWS_REGION=""  # e.g., us-east-1
YOUR_AWS_ACCOUNT_ID=""

echo "🚀 Step 1: Rebuild Docker image"
docker build -t "$IMAGE_NAME" .

echo "✅ Image built successfully!"

echo "🔐 Step 2: Log in to AWS ECR"
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin YOUR_AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com

echo "🏷 Step 3: Tag image for ECR"
docker tag "$IMAGE_NAME":latest YOUR_AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com/pictures2stories:latest

echo "📤 Step 4: Push image to ECR"
docker push YOUR_AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com/pictures2stories:latest

echo "🎉 Deployment complete!"
