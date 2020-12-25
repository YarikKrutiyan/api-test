#FROM python:3.6-slim
#COPY . /api-test
#WORKDIR /api-test
#RUN pwd
#RUN ls
#RUN pwd
##RUN pip3 install -r requirements.txt
#RUN pip3 install attrs binary certifi chardet idna iniconfig packaging pluggy psycopg2-binary py pyparsing pytest requests toml urllib3
#
#RUN ["pytest", "-v", "tests","--junitxml=reports/result.xml"]
#CMD tail -f /dev/null

FROM alpine
COPY . /api-test
WORKDIR /api-test
RUN apk add --update-cache curl wget busybox-extras netcat-openbsd python3 py-pip
RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip3 install awscli
CMD pip3 install requirements.txt
RUN pwd
RUN ls
#CMD pytest -v --junitxml=reports/result.xml /tests
CMD ["pytest", "-v", "tests","--junitxml=reports/result.xml"]

CMD tail -f /dev/null