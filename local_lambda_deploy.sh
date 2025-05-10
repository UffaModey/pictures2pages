#!/bin/bash

# Set variables
FUNCTION_PAYLOAD='{
  "image_1": "media_files/first_image.jpg",
  "image_2": "media_files/second_image.jpg",
  "image_3": "media_files/third_image.jpg",
  "theme": "adventure",
  "type": "poem"
}'
CONTAINER_NAME="pictures2pages_lambda_container"
IMAGE_NAME="pictures2pages_lambda"
PORT="9000"

echo "🚀 Step 1/4: Rebuild Docker image"
docker build -t $IMAGE_NAME .

echo "✅ Image built successfully!"

# Check for existing container using port 9000 and remove it
EXISTING_CONTAINER_ID=$(docker ps -q --filter "name=$CONTAINER_NAME")

if [ -n "$EXISTING_CONTAINER_ID" ]; then
  echo "🛑 Stopping and removing existing container..."
  docker stop $CONTAINER_NAME
  docker rm $CONTAINER_NAME
else
  echo "ℹ️ No existing container found on port $PORT."
fi

echo "🛠 Step 2/4: Run new container"
docker run -d --name $CONTAINER_NAME -p 9000:8080 --env-file .env $IMAGE_NAME

echo "⏳ Step 3/4: Waiting for container to start..."
sleep 5

echo "🔍 Step 4/4: Test function in the container"
curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" \
     -H "Content-Type: application/json" \
     -d "$FUNCTION_PAYLOAD"

echo ""
echo "🎉 Deployment complete!"
