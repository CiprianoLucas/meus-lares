#!/bin/bash
cd /home/ubuntu/meus-lares/
docker-compose -f docker-compose.prod.yml down
sudo rm -rf /api/static
. .env
cd interface
[ -n "$VITE_API_URL" ] && echo "VITE_API_URL=${VITE_API_URL}" > .env
npm i
sudo npm run build
cd ..
docker-compose -f docker-compose.prod.yml up -d --build
exit 0