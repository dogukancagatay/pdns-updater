FROM python:3.8.5-alpine
LABEL maintainer="Doğukan Çağatay <dcagatay@gmail.com>"

ENV PDNS_API_URL "http://pdns:8081/api/v1"
ENV PDNS_API_KEY "changeme"

WORKDIR /app
COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY ./ /app

VOLUME [ "/var/run/docker.sock" ]

CMD [ "python", "main.py" ]
