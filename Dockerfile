FROM python:3.10.12

RUN mkdir -p /usr/src/app/
RUN mkdir -p /usr/src/app/src/logs/
WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app/

RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

EXPOSE 8000

CMD ["/bin/sh", "./scripts/start.sh"]