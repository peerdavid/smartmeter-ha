# syntax=docker/dockerfile:1

FROM python:3-slim-buster

WORKDIR /usr/src/app

COPY ./src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

ENV TERM=xterm

CMD [ "python", "ha_bridge.py", "--log_console", "True"]
