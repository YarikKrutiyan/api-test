FROM alpine
RUN apk add --update-cache curl wget busybox-extras netcat-openbsd python3 py-pip
RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip install awscli
RUN pip install requirements.txt
RUN pytest tests/test_api/test_catalog_agrojob
CMD tail -f /dev/null