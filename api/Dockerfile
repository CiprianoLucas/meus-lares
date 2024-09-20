FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install poetry
RUN poetry install --with prod
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "meus_lares.wsgi:application"]