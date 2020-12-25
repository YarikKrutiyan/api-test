#FROM python:3.6-slim
#COPY . /api-test
#WORKDIR /api-test
#RUN apk add --update-cache curl wget busybox-extras netcat-openbsd python3 py-pip



FROM python:3.6-slim
COPY . /api-test
WORKDIR /api-test
RUN pwd
RUN ls -AL

#1111212

CMD pip3 install --no-cache-dir -r /requirements.txt
RUN pip3 install pytest
RUN ls -Al
RUN pytest -v tests/api_test/test_get_lands.py --junitxml=reports/result.xml
#CMD pytest  -v  /workspace/tests/test_api/test_catalog_culture_list.py --junitxml=/reports/result.xml
#RUN python3 -m venv venv
#RUN source venv/bin/activate
#CMD pip3 install requirements.txt
#CMD venv/bin/pytest  -v  tests/test_api/test_catalog_culture_list.py --junitxml=reports/result.xml

#CMD ["pytest", "-v", "tests","--junitxml=reports/result.xml"]

CMD tail -f /dev/null