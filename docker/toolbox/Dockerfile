FROM python:3.6-slim
COPY . /api-test
WORKDIR /api-test
CMD /api-test
RUN pip install --no-cache-dir -r requirements.txt
RUN ["pytest", "-v", "--junitxml=reports/result.xml"]
CMD tail -f /dev/null