#!/bin/bash
set -e  # Exit on any error

echo "🔨 Building discretelog API..."

# Step 1: Build Go binary for Linux
echo "📦 Building Go binary for Linux amd64..."
GOOS=linux GOARCH=amd64 go build -o discretelog-server .

# Step 2: Build and push Docker container
echo "🐳 Building Docker container..."
docker buildx build \
  --platform linux/amd64 \
  -f Dockerfile.prod \
  -t ghcr.io/qiumatthew/website-discretelog:latest \
  --push \
  --progress=plain \
  .

echo "✅ Build complete! Image pushed to GitHub Container Registry"
echo "📦 Image: ghcr.io/qiumatthew/website-discretelog:latest"
echo ""
echo "To deploy on VM:"
echo "  Update docker-compose.yml in deployment repo"
echo "  docker compose pull && docker compose up -d"