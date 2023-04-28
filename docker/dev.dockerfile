FROM ubuntu:22.04

RUN apt update && apt install -y python3-pip python3-setuptools python3-dev

# Install requirements for tests
COPY requirements.txt /opt/engin/requirements.txt
COPY requirements-dev.txt /opt/engin/requirements-dev.txt
RUN python3 -m pip install \
  -r /opt/engin/requirements.txt \
  -r /opt/engin/requirements-dev.txt

ENV PYTHONPATH /opt/engin

# This is mounted in the docker-compose file.
WORKDIR /opt/engin
ENTRYPOINT bash