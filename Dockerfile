#FROM python:3.7-alpine
FROM amazonlinux
LABEL author="mikebrumfield30@gmail.com"
WORKDIR /twitterStreamer
COPY requirements.txt .
COPY creds.py .
COPY streamTwitter.py .
COPY sqs.py .
COPY dynamoDB.py .
COPY secretsManager.py .
COPY filtered_stream.py .
COPY execute_timed_ingestion.sh .
COPY docker_exec.sh .
RUN sh docker_exec.sh
ENTRYPOINT ["bash",  "execute_timed_ingestion.sh"]