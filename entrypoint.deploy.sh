#!/bin/bash
cd /home/ubuntu/meus-lares/
docker-compose -f docker-compose.prod.yml down
. .env
cd interface
npm i
npm run build
cd ..
docker-compose -f docker-compose.prod.yml up -d --build
exit 0