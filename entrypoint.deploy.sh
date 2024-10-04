#!/bin/bash
cd /home/ubuntu/meus-lares/
docker-compose -f docker-compose.prod.yml down
sudo rm -rf /api/static
. .env
cd interface
npm i
sudo npm run build
cd ..
docker-compose -f docker-compose.prod.yml up -d --build
exit 0