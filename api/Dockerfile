FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 9000
CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]