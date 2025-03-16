#! /bin/bash
set -a
source .env.production
set +a

gcloud compute ssh app@$GOOGLE_CLOUD_PROJECT_ID --zone=$ZONE --command "
    sudo su
    cd /home/app/meus-lares
    git reset --hard origin/develop
    cd api
    source venv/bin/activate
    poetry install
    python3 manage.py migrate
    sudo systemctl restart meus-lares
    sudo systemctl restart nginx
    exit
"