FROM python:3.6.4-slim

WORKDIR /plagiarism_detection/server

ADD entrypoint.sh ./
RUN set -ex && \
    chmod +x entrypoint.sh

ADD requirements.txt ./

RUN set -ex && \
    pip install -r requirements.txt

ADD ./ ./

RUN set -ex && \
    nosetests --with-coverage --cover-erase --cover-package=server -v

ENTRYPOINT ["./entrypoint.sh"]
