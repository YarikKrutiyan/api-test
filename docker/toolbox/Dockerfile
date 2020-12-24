FROM alpine
RUN apk add --update-cache curl wget busybox-extras netcat-openbsd python3 py-pip
RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip3 install awscli
RUN pip3 install attrs
RUN pip3 install binary
RUN pip3 install certifi
RUN pip3 install chardet
RUN pip3 install idna
RUN pip3 install iniconfig
RUN pip3 install packaging
RUN pip3 install pluggy
#RUN pip3 install psycopg2
RUN pip3 install py
RUN pip3 install pyparsing
RUN pip3 install pytest
RUN pip3 install requests
RUN pip3 install toml
RUN pip3 install urllib3
#CMD pip3 install -r requirements.txt
CMD pytest /tests/test_api/test_catalog_agrojob
CMD tail -f /dev/null