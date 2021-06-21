import requests
import json
import creds
import logging
from secretsManager import get_secret
from dynamoDB import index_tweet
from filtered_stream import connect_to_stream_and_ingest


logger = logging.getLogger("twitter stream")
logger.setLevel(logging.INFO)

endpoint = "https://api.twitter.com/2/tweets/sample/stream"
auth = get_secret()
token = auth['bearerToken']
headers = {"Authorization": "Bearer {}".format(token)}


def connect_to_endpoint(url):
    response = requests.request("GET", url, headers=headers, stream=True)
    print(response.status_code)
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            tweet = json_response["data"]
            index_tweet(tweet, 'RawTweets')
            # print(tweet)
            # logger.log(json.dumps(json_response, indent=4, sort_keys=True))
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )


def main():
    # connect_to_endpoint(endpoint)
    topic = 'phoenix suns'
    logger.info(f"Running stream for {topic}")
    connect_to_stream_and_ingest(topic)
    

if __name__ == "__main__":
    main()
