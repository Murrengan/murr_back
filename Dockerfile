FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /murr_workdir_for_docker
RUN mkdir /murr_postgresql_data_volumes
RUN mkdir /murr_nginx_data_volume
WORKDIR /murr_workdir_for_docker

COPY requirements.txt /murr_workdir_for_docker/
RUN pip install -r requirements.txt

COPY . /murr_workdir_for_docker/