#!/bin/bash
cd /home/ubuntu/meus-lares/
. .env
docker-compose -f docker-compose.prod.yml up -d
exit 0