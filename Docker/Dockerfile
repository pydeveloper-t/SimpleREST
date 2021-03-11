FROM python:3.8
MAINTAINER Andrey Tikhonov "andrey.tikhonov@ukr.net"

RUN apt-get update
RUN apt-get install git curl -y
RUN bash -c 'git clone https://github.com/pydeveloper-t/SimpleREST.git ; pip3 install -r /SimpleREST/requirements.txt'
WORKDIR /SimpleREST/app
ENTRYPOINT ["/SimpleREST/app/start.sh"]