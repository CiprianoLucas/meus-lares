#! /bin/bash
set -a
source .env.production
set +a

cp .env.production api/.env

cd interface
[ -n "$URL_BACK" ] && echo "VITE_API_URL=${URL_BACK}" > .env.production
[ -n "$GOOGLE_CLIENT_ID" ] && echo "VITE_GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}" >> .env.production


npm run build
cd ..
python3 api/manage.py collectstatic --noinput

rm api/.env