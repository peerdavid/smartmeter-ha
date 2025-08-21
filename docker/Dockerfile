# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY ../tools/setup.sh /tmp/setup.sh
RUN /tmp/setup.sh

COPY ../requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ../src .

CMD [ "python3", "-m" , "ha_bridge.py", "run", "--host=0.0.0.0"]