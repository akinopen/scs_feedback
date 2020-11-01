FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc gettext && rm -rf /var/lib/apt/lists/* && pip install --upgrade pip setuptools wheel

RUN mkdir /app
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app/
ENTRYPOINT ["./docker-entrypoint.sh"]
