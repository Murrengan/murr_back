FROM python:3.7-slim
WORKDIR /home/murrengan

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt /home/murrengan/requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN apt-get update && apt-get install netcat -y

COPY . /home/murrengan

ENTRYPOINT ["/home/murrengan/entrypoint.sh"]
