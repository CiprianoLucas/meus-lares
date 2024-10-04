#!/bin/bash
cd "$(dirname "$0")"
. .env
sudo docker-compose -f docker-compose.prod.yml up
exit 0