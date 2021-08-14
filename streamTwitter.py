import requests
import json
import creds
import logging
from secretsManager import get_secret
from filtered_stream import connect_to_stream_and_ingest
import os


logger = logging.getLogger("twitter stream")
logger.setLevel(logging.INFO)

endpoint = "https://api.twitter.com/2/tweets/sample/stream"
auth = get_secret()
token = auth['bearerToken']
headers = {"Authorization": "Bearer {}".format(token)}


def main():
    topic = os.getenv('TOPIC')
    print(f"Topic is {topic}")
    logger.info(f"Running stream for {topic}")
    connect_to_stream_and_ingest(topic)
    

if __name__ == "__main__":
    main()
