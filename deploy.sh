#!/bin/bash
# meus-lares
cd /home/ubuntu/meus-lares
git reset --hard origin/main
git pull
. ./entrypoint.deploy.sh
exit