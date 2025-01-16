#!/bin/bash
cd /home/ubuntu/meus-lares/
docker compose -f docker-compose.prod.yml down
rm -rf ./api/static
. .env
cd interface
[ -n "$URL_BACK" ] && echo "VITE_API_URL=${URL_BACK}" > .env
[ -n "$GOOGLE_CLIENT_ID" ] && echo "VITE_GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}" >> .env
npm i
npm run build
cd ..
docker compose -f docker-compose.prod.yml up -d --build
exit 0