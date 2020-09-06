FROM python:3.7-slim
WORKDIR /home/murrengan

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y build-essential netcat git gcc \
  && apt-get install -y libpq-dev \
  && apt-get install -y gettext \
  && pip install --upgrade pip \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt /home/murrengan/requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . /home/murrengan

ENTRYPOINT ["/home/murrengan/entrypoint.sh"]
