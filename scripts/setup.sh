#!/bin/bash
set -e

echo "Setting up WhatsApp Web Clone..."

# Create .env files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start services
docker-compose up -d

echo "Services started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
