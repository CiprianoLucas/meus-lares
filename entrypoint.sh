#!/bin/bash
cd "$(dirname "$0")"
. .env
docker-compose -f docker-compose.prod.yml up
exit 0