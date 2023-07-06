# base images
FROM ubuntu:20.04
FROM python:3.8
FROM mysql:8.0.18
FROM gcc:latest

ENV PATH="/usr/local/bin:${PATH}"

RUN apt-get update && apt-get install -y python3 python3-pip
# maintainer
# LABEL maintainer 

WORKDIR /Web_Application_Project
COPY requirements.txt .

RUN pip3 install -r requirements.txt --break-system-packages


EXPOSE 8000

WORKDIR /Web_Application_Project

CMD ["python3", "manage.py", "makemigrations"]
CMD ["python3", "manage.py", "migrate"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# RUN python3 manage.py makemigrations
# RUN python3 manage.py migrate
# RUN python3 manage.py runserver 0.0.0.0:8000