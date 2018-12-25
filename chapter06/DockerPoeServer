FROM python:3.5
MAINTAINER Channel Cat <channelcat@gmail.com>

ADD . /code
RUN pip3 install git+https://github.com/channelcat/sanic
RUN pip3 install Savoir
RUN pip3 install Sanic-Cors

EXPOSE 8000

WORKDIR /code

CMD ["python", "poe_server.py"]