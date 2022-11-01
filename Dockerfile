FROM python:3.10.7-alpine

WORKDIR /code
RUN apk update \
    && apk add mariadb-dev \
    gcc\
    python3-dev \
    pango-dev \
    cairo-dev \
    libtool \
    linux-headers \
    musl-dev \
    libffi-dev \
    openssl-dev \
    jpeg-dev \
    zlib-dev

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN python -m pip install --upgrade pip

COPY requirements.txt /code/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/
EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]