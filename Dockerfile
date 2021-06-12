FROM python:3.7-alpine
LABEL author="mikebrumfield30@gmail.com"
RUN pip install --upgrade pip
WORKDIR /twitterStreamer
COPY requirements.txt .
COPY creds.py .
COPY streamTwitter.py .
COPY dynamoDB.py .
COPY secretsManager.py .
COPY filtered_stream.py .
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3",  "streamTwitter.py"]
