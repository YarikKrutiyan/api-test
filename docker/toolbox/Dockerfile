FROM python:3.6-slim
COPY . /api-test
WORKDIR /api-test
RUN apk add --update-cache curl wget busybox-extras netcat-openbsd python3 py-pip
RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip3 install awscli
CMD pip3 install requirements.txt
#CMD venv/bin/pytest  -v  tests/test_api/test_catalog_culture_list.py --junitxml=reports/result.xml

#CMD ["pytest", "-v", "tests","--junitxml=reports/result.xml"]

CMD tail -f /dev/null