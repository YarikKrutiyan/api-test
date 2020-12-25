FROM python:3.6-slim
COPY . /api-test
WORKDIR /api-test
RUN pwd
RUN ls
RUN pwd
#RUN pip3 install -r requirements.txt
RUN pip3 install attrs binary certifi chardet idna iniconfig packaging pluggy psycopg2-binary py pyparsing pytest requests toml urllib3

RUN ["pytest", "-v", "tests","--junitxml=reports/result.xml"]
CMD tail -f /dev/null