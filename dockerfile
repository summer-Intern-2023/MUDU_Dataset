# base images
FROM ubuntu:20.04
FROM python:3.8
FROM mysql:8.0.18
FROM gcc:13.1

ENV PATH="/usr/local/bin:${PATH}"

RUN apt-get update && apt-get install -y python3 python3-pip
# maintainer
# LABEL maintainer 

WORKDIR /Web_Application_Project
COPY . /Web_Application_Project
VOLUME /sqlitedb

RUN pip3 install -r requirements.txt --break-system-packages 

# if you make this file in China, you can try to change the command below
# RUN pip3 install -r requirements.txt --break-system-packages -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["python3", "manage.py", "makemigrations"]
CMD ["python3", "manage.py", "migrate"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# RUN python3 manage.py makemigrations
# RUN python3 manage.py migrate
# RUN python3 manage.py runserver 0.0.0.0:8000

# docker build -t llmdataset:3.0 . -f dockerfile
# docker run -d -p 80:8000  llmdataset:3.0
