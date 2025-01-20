#!/bin/bash

# Step 1: Build the Docker image
docker build -t inventory-manager .

# Step 2: Run tests inside the Docker container
docker run --rm inventory-manager python3 -m pytest tests/

# Step 3: Run the application in the background
docker run -d --name inventory-manager-app -p 5000:5000 inventory-manager

# Step 4: Test the connection
curl http://localhost:5000
echo "Application is running at: http://localhost:5000"
