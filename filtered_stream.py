import requests
import json
from secretsManager import get_secret
import logging
from dynamoDB import index_tweet


logger = logging.getLogger("filteredTwitterStream")
logger.setLevel(logging.INFO)
auth = get_secret()
token = auth['bearerToken']
headers = {"Authorization": "Bearer {}".format(token)}
rules_endpoint = "https://api.twitter.com/2/tweets/search/stream/rules"


def set_rule(topic):
    rule = {
        "add": [
            {
                "value": f"{topic} -has:media",
                "tag": f"{topic} without media"
            }
        ]
    }
    response = requests.request("POST", rules_endpoint, headers=headers, data=json.loads(rule))
    return response.status_code


def get_all_rules():
    rules = []
    response = requests.request("GET", rules_endpoint, headers=headers)
    response_json = response.json()
    data = response_json['data']
    for rule in data:
        rules.append(rule['id'])
    return rules


def clear_existing_rules():
    existing_rules = get_all_rules()
    rule = {
        "delete": {
            "ids": existing_rules
        }
    }
    response = requests.request("POST", rules_endpoint, headers=headers, data=json.loads(rule))
    return response.status_code


def connect_to_stream_and_ingest(topic):
    clear_existing_rules()
    set_rule(topic)
    url = "https://api.twitter.com/2/tweets/search/stream"
    response = requests.request("GET", url, headers=headers, stream=True)
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            tweet = json_response["data"]
            # index_tweet(tweet)
            logger.info(tweet)