# syntax=docker/dockerfile:1
FROM python:3.10.12
ENV HOST 0.0.0.0
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . .
EXPOSE 8000
RUN pip install -r requirements.txt
ENTRYPOINT ["/bin/sh", "-c" , "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]


