FROM alpine
RUN apk add --no-cashe curl wget busybox-extras netcat-openbsd python py-pip python3-venv
RUN python3 -m venv env
RUN source env/bin/activate
RUN pip install awscli
RUN pip install requirements.txt
RUN pytest tests/test_api/test_catalog_agrojob
CMD tail -f /dev/null