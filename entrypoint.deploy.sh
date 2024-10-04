#!/bin/bash
cd "$(dirname "$0")"
. .env
cd interface
npm i
sudo npm run build
cd ..
sudo docker-compose -f docker-compose.prod.yml up -d --build
exit 0