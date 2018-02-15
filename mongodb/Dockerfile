FROM ubuntu:xenial

RUN set -ex && \
    apt-get update && \
    apt-get install -y gnupg

RUN set -ex && \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 \
    --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
RUN set -ex && \
    echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" \
    | tee /etc/apt/sources.list.d/mongodb-org-3.6.list

RUN set -ex && \
    apt-get update && \
    apt-get install -y mongodb

RUN set -ex && \
    mkdir -p /data/db

EXPOSE 27017

ENTRYPOINT ["/usr/bin/mongod"]
