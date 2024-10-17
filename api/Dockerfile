FROM python:3.12-slim
WORKDIR /app

COPY ./api /app
COPY ./.env /app/venv/
COPY ./api/crontab /etc/cron.d/tasks-cron
COPY ./api/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN chmod +x /app/start_django.sh

RUN apt-get update && apt-get -y install cron supervisor

RUN chmod 0644 /etc/cron.d/tasks-cron
RUN crontab /etc/cron.d/tasks-cron
RUN touch /var/log/cron.log /var/log/django.log

RUN pip install poetry
RUN poetry install --with prod


CMD ["/usr/bin/supervisord"]
