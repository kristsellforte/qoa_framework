FROM python:3.6.8-jessie

COPY requirements.txt /

# will be overwriten should `docker run` pass a proper env
ENV EXECUTION_ID 111111

RUN mkdir main

COPY performance_monitor.py ./main/performance_monitor.py
COPY credentials.py ./main/credentials.py
COPY store.py ./main/store.py
COPY utils.py ./main/utils.py
