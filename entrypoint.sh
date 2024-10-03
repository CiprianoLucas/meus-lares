#!/bin/bash
cd "$(dirname "$0")"
git pull
cd interface
npm i
npm run build
cd ..
docker-compose -f docker-compose.prod.yml up -d --build
exit 0