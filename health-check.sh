#!/bin/bash

# Debot Health Check Script
# This script checks the health of all services and provides working URLs

echo "===== DEBOT HEALTH CHECK ====="

# Get service information
LANDO_INFO=$(lando info --format=json)

# Function to check URL accessibility
check_url() {
  URL="$1"
  SERVICE_NAME="$2"
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
  
  if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 400 ]; then
    echo "✅ $SERVICE_NAME is accessible at $URL (HTTP $HTTP_CODE)"
    return 0
  else
    echo "❌ $SERVICE_NAME returned HTTP $HTTP_CODE at $URL"
    return 1
  fi
}

# Extract frontend URL
echo ""
echo "Checking Frontend..."
FRONTEND_URL=$(echo "$LANDO_INFO" | grep -o '"http://debot.lndo.site"' | tr -d '"')
FRONTEND_LOCAL_URL=$(echo "$LANDO_INFO" | grep -o '"http://localhost:[0-9]*"' | grep -v 8000 | grep -v 8081 | head -1 | tr -d '"')

if [ -n "$FRONTEND_URL" ]; then
  check_url "$FRONTEND_URL" "Frontend (Lando domain)"
fi

if [ -n "$FRONTEND_LOCAL_URL" ]; then
  check_url "$FRONTEND_LOCAL_URL" "Frontend (localhost)"
fi

# Extract backend URL
echo ""
echo "Checking Backend..."
BACKEND_URL=$(echo "$LANDO_INFO" | grep -o '"http://api.debot.lndo.site:[0-9]*"' | tr -d '"')
BACKEND_LOCAL_URL=$(echo "$LANDO_INFO" | grep -o '"http://localhost:8000"' | tr -d '"')

if [ -n "$BACKEND_URL" ]; then
  check_url "$BACKEND_URL" "Backend (Lando domain)"
fi

if [ -n "$BACKEND_LOCAL_URL" ]; then
  check_url "$BACKEND_LOCAL_URL" "Backend (localhost)"
fi

# Check MongoDB
echo ""
echo "Checking MongoDB..."
MONGO_CONTAINER=$(docker ps | grep debot_database | awk '{print $1}')
if [ -n "$MONGO_CONTAINER" ]; then
  echo "✅ MongoDB container is running"
  # Get the mapped port for MongoDB
  MONGO_PORT=$(docker port $MONGO_CONTAINER 27017/tcp | cut -d ':' -f 2)
  if [ -n "$MONGO_PORT" ]; then
    echo "✅ MongoDB is accessible at localhost:$MONGO_PORT"
    # Try to connect to MongoDB
    if docker exec $MONGO_CONTAINER mongosh --quiet --eval "db.stats()" > /dev/null 2>&1; then
      echo "✅ MongoDB connection successful"
    else
      echo "❌ MongoDB connection failed (but container is running)"
    fi
  else
    echo "❌ MongoDB port mapping not found"
  fi
else
  echo "❌ MongoDB container is not running"
fi

# Summary of working URLs
echo ""
echo "===== WORKING URLS ====="
if [ -n "$FRONTEND_LOCAL_URL" ]; then
  echo "Frontend: $FRONTEND_LOCAL_URL"
fi
if [ -n "$FRONTEND_URL" ]; then
  echo "Frontend: $FRONTEND_URL"
fi
if [ -n "$BACKEND_LOCAL_URL" ]; then
  echo "Backend: $BACKEND_LOCAL_URL"
fi
if [ -n "$BACKEND_URL" ]; then
  echo "Backend: $BACKEND_URL"
  echo "Backend API Docs: ${BACKEND_URL}/docs"
fi
echo ""
echo "===== MongoDB Connection Info ====="
if [ -n "$MONGO_PORT" ]; then
  echo "MongoDB Connection String: mongodb://localhost:$MONGO_PORT"
  echo "MongoDB Client Connection:"
  echo "  Host: localhost"
  echo "  Port: $MONGO_PORT"
  echo "  Database: debot"
  echo "  No authentication required"
else
  echo "MongoDB Connection: Not available"
fi

echo ""
echo "If Lando domain URLs are not working, run: sudo ./setup-hosts.sh" 