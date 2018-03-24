FROM python:3.6.4-slim

WORKDIR /plagiarism_detection/server

RUN apt-get update && \
    apt-get install -y gcc

ADD entrypoint.sh ./
RUN set -ex && \
    chmod +x entrypoint.sh

ADD requirements.txt ./

RUN set -ex && \
    pip3 install -r requirements.txt

ADD ./ ./

RUN set -ex && \
    nosetests --with-coverage --cover-erase --cover-package=server -v

ENTRYPOINT ["./entrypoint.sh"]
