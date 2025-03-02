#!/bin/bash

# This script adds local host entries for Lando development

# Check if script is run with sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script with sudo: sudo ./setup-hosts.sh"
  exit 1
fi

# Get the current Docker host IP (usually 127.0.0.1)
DOCKER_IP="127.0.0.1"

# Domains to add
DOMAINS=(
  "debot.lndo.site"
  "api.debot.lndo.site"
  "mongo.debot.lndo.site"
)

# Backup hosts file
cp /etc/hosts /etc/hosts.backup.$(date +%Y%m%d%H%M%S)
echo "Backed up hosts file"

# Check if entries already exist and add if not
for DOMAIN in "${DOMAINS[@]}"; do
  if grep -q "$DOMAIN" /etc/hosts; then
    echo "$DOMAIN already exists in hosts file"
  else
    echo "$DOCKER_IP $DOMAIN" >> /etc/hosts
    echo "Added $DOMAIN to hosts file"
  fi
done

echo "Host entries setup complete!"
echo "Your Lando sites should now be accessible at:"
echo "  - Frontend: http://debot.lndo.site"
echo "  - Backend API: http://api.debot.lndo.site"
echo "  - MongoDB UI: http://mongo.debot.lndo.site"
echo ""
echo "If you still have issues, try running 'sudo killall -HUP mDNSResponder' to flush DNS cache" 