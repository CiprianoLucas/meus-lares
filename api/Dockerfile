FROM python:3.12-slim
WORKDIR /app

COPY . /app

RUN pip install poetry
RUN poetry install --with prod
RUN apt-get update && apt-get -y install cron supervisor

COPY crontab /etc/cron.d/daily-tasks-cron

RUN chmod 0644 /etc/cron.d/daily-tasks-cron
RUN crontab /etc/cron.d/daily-tasks-cron
RUN touch /var/log/cron.log /var/log/django.log

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]
