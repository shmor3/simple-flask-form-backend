FROM ubuntu:latest
ENV CI=true
RUN apt-get update
RUN apt-get -y install \
    python3 \
    python3-pip
RUN pip install cryptocode Flask
COPY . .