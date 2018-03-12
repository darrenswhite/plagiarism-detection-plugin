FROM mongo:3.6.3

COPY entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh

EXPOSE 27017

ENTRYPOINT ["/tmp/entrypoint.sh"]
