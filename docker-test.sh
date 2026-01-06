#!/bin/bash
# SignalPilot CLI - Docker Testing Script

set -e

echo "🐳 SignalPilot CLI - Docker Test Environment"
echo "============================================"
echo ""

# Build the Docker image
echo "📦 Building Docker image..."
docker compose build

# Start the container
echo "🚀 Starting container..."
docker compose up -d

# Wait for container to be ready
sleep 2

# Open interactive shell
echo "✓ Container ready!"
echo ""
echo "📝 Quick start commands:"
echo "  sp --help              # View CLI help"
echo "  sp init                # Initialize workspace"
echo "  sp lab --port 9999     # Launch Jupyter Lab"
echo ""
echo "🌐 Access Jupyter Lab at: http://localhost:9999"
echo ""
echo "💡 Note: Code is copied during build. Run './docker-test.sh' again to test changes."
echo ""
echo "Entering container shell..."
docker compose exec sp-cli-dev /bin/bash
