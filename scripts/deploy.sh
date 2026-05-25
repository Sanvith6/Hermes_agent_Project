#!/bin/bash
set -e

echo "Deploying WhatsApp Web Clone..."

# Build images
docker-compose build

# Deploy
docker-compose up -d

echo "Deployment complete!"
