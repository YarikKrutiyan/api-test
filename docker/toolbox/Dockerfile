FROM alpine
RUN apk add --update-cache curl wget busybox-extras netcat-openbsd python3 py-pip
RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip3 install awscli
CMD pytest /tests/test_api/test_catalog_agrojob
CMD tail -f /dev/null
CMD docker rm $(docker ps -a -q)