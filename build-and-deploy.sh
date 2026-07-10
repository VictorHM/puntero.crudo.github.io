#!/bin/bash
# Deploy blog to production server
# Usage: ./deploy.sh

set -e

REMOTE_USER="bloguser"
REMOTE_HOST="punterocrudo"
REMOTE_PATH="/var/www/punterocrudo"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Building blog...${NC}"
python3 build.py

if [ ! -d "output" ]; then
    echo -e "${RED}❌ Error: output/ folder not found. Did build.py run successfully?${NC}"
    exit 1
fi

echo -e "${YELLOW}📡 Deploying to ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}${NC}"

# Deploy complete output folder to server
rsync -avz --delete \
    output/ \
    "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/"

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo -e "${YELLOW}Visit: http://punterocrudo.com${NC}"
