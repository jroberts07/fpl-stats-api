FROM python:3.6-alpine3.7

WORKDIR /usr/src/app
ENV PYTHONPATH /usr/src/app

RUN apk add --update --no-cache --virtual .build-deps \
        build-base \
        python-dev \
        libxml2 \
        libxml2-dev && \
    apk add libxslt-dev py3-lxml

COPY requirements.txt /usr/src/app/requirements.txt

RUN pip3 install --no-use-pep517 --no-cache-dir -r requirements.txt

RUN apk --purge del .build-deps

COPY . ./

CMD ["python", "server.py"]
