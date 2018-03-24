FROM python:3.6.4-slim

WORKDIR /plagiarism_detection/postprocessor

ADD entrypoint.sh ./
RUN set -ex && \
    chmod +x entrypoint.sh

ADD requirements.txt ./

RUN set -ex && \
    pip3 install -r requirements.txt

ADD ./ ./

RUN set -ex && \
    nosetests --with-coverage --cover-erase --cover-package=postprocessor -v

ENTRYPOINT ["./entrypoint.sh"]
