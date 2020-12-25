FROM alpine
RUN apk add --update-cache curl wget busybox-extras netcat-openbsd python3 py-pip
RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip3 install awscli
CMD pip3 install requirements.txt
#CMD tail -f /dev/null
