#! /bin/bash

# Carregar variáveis do .env
set -a
source .env.production
set +a

# Carregar credenciais
export SSH_PRIVATE_KEY="$(cat id_ed25519)"
export GCLOUD_CREDENCIAL="$(cat api/$GOOGLE_APPLICATION_CREDENTIALS)"

# Criar a instância no Google Cloud
gcloud compute instances create $INSTANCE_NAME \
    --project=meus-lares \
    --zone=$ZONE \
    --machine-type=$MACHINE_TYPE \
    --network-interface=address=35.211.143.242,network-tier=STANDARD,stack-type=IPV4_ONLY,subnet=default \
    --metadata=startup-script="#! /bin/bash
        sudo apt update && sudo apt install -y python3 python3-venv python3-pip git nginx certbot python3-certbot-nginx

        # Criar usuário para rodar a aplicação
        sudo useradd -m app

        sudo -u app bash -c \"
            # Configuração SSH para clonar repositório privado
            mkdir -p /home/app/.ssh
            echo \"$SSH_PRIVATE_KEY\" | tee /home/app/.ssh/id_ed25519 > /dev/null
            chmod 600 /home/app/.ssh/id_ed25519
            echo -e \"Host github.com\n    IdentityFile /home/app/.ssh/id_ed25519\n    StrictHostKeyChecking no\" | tee /home/app/.ssh/config > /dev/null
            chmod 600 /home/app/.ssh/config

            # Clonar repositório
            git clone git@github.com:CiprianoLucas/meus-lares.git /home/app/meus-lares
            cd /home/app
            cd meus-lares
            git checkout -b develop origin/develop
            cd api
            python3 -m venv venv
            source venv/bin/activate
            pip install poetry
            poetry install --with prod

            # Criar arquivo .env com variáveis de ambiente

            tee /home/app/meus-lares/api/.env > /dev/null <<EOF
            # Django
            ENV=$ENV
            URL_BACK=$URL_BACK
            URL_FRONT=$URL_FRONT
            SECRET_KEY=$SECRET_KEY
            API_PORT=$API_PORT

            # Database
            DB_NAME=$DB_NAME
            DB_USER=$DB_USER
            DB_PASSWORD=$DB_PASSWORD
            DB_HOST=$DB_HOST
            DB_PORT=$DB_PORT

            # Vue3
            GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID
            INTERFACE_PORT=$INTERFACE_PORT

            # GOOGLE
            GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS
            GOOGLE_CLOUD_PROJECT_ID=$GOOGLE_CLOUD_PROJECT_ID
            GS_BUCKET_MEDIA=$GS_BUCKET_MEDIA
            GS_BUCKET_STATIC=$GS_BUCKET_STATIC

            # Email
            EMAIL_HOST=$EMAIL_HOST
            EMAIL_PORT=$EMAIL_PORT
            EMAIL_USE_TLS=$EMAIL_USE_TLS
            EMAIL_USE_SSL=$EMAIL_USE_SSL
            EMAIL_HOST_USER=$EMAIL_HOST_USER
            EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD

            # Docker
            IS_DOCKER=$IS_DOCKER
EOF
            echo '$GCLOUD_CREDENCIAL' | tee /home/app/meus-lares/api/$GOOGLE_APPLICATION_CREDENTIALS > /dev/null
        \"

        # Criar serviço systemd para rodar Django com Gunicorn
        sudo tee /etc/systemd/system/meus-lares.service > /dev/null <<EOF
        [Unit]
        Description=Meus Lares Django API
        After=network.target

        [Service]
        User=app
        Group=app
        WorkingDirectory=/home/app/meus-lares/api
        ExecStart=/home/app/meus-lares/api/venv/bin/gunicorn --workers 3 --bind unix:/home/app/meus-lares/api/meus-lares.sock meus_lares.wsgi:application
        Restart=always

        [Install]
        WantedBy=multi-user.target
EOF

        # Ativar e iniciar o serviço do Django
        sudo systemctl daemon-reload
        sudo systemctl enable meus-lares
        sudo systemctl start meus-lares

        # Configurar Nginx
        sudo tee /etc/nginx/sites-available/meus-lares > /dev/null <<EOF
        server {
            listen 80;
            server_name $URL_BACK;

            return 301 https://\$host\$request_uri;

            location / {
                include proxy_params;
                proxy_pass http://unix:/home/app/meus-lares/api/meus-lares.sock;
            }
        }
        server {
            listen 443 ssl;
            server_name meus-lares.com;

            ssl_certificate /etc/letsencrypt/live/meus-lares.com/fullchain.pem;
            ssl_certificate_key /etc/letsencrypt/live/meus-lares.com/privkey.pem;
            include /etc/letsencrypt/options-ssl-nginx.conf;
            ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

            location / {
                include proxy_params;
                proxy_pass http://unix:/home/app/meus-lares/api/meus-lares.sock;
            }
        }
EOF

        sudo ln -s /etc/nginx/sites-available/meus-lares /etc/nginx/sites-enabled/
        sudo systemctl restart nginx

        # Configurar HTTPS com Let's Encrypt
        sudo certbot --nginx --non-interactive --agree-tos --redirect -d $URL_BACK -m $EMAIL_HOST_USER
        sudo systemctl restart nginx
    " \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=286732687358-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append \
    --tags=https-server \
    --create-disk=auto-delete=yes,boot=yes,device-name=meus-lares,image=projects/debian-cloud/global/images/debian-12-bookworm-v20250311,mode=rw,size=10,type=pd-standard \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ec-src=vm_add-gcloud \
    --reservation-affinity=any
