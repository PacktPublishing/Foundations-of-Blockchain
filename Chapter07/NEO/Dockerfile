FROM ubuntu:latest

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \

  && pip3 install --upgrade pip
RUN apt-get install -y libleveldb-dev libssl-dev g++
RUN pip install neo-python==0.6.9

ADD . /code

WORKDIR /code
