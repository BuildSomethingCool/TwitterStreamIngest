import sys

import requests
import json
from secretsManager import get_secret
import logging
from dynamoDB import index_tweet, create_landing_table
import creds


logger = logging.getLogger("filteredTwitterStream")
logger.setLevel(logging.INFO)
if creds.env == 'dev':
    token = creds.api_details['bearerToken']
else:
    auth = get_secret()
    token = auth['bearerToken']
headers = {"Authorization": "Bearer {}".format(token)}
rules_endpoint = "https://api.twitter.com/2/tweets/search/stream/rules"


def set_rules(topic):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": f"{topic}", "tag": f"{topic}"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def connect_to_stream_and_ingest(topic):
    rules = get_rules()
    delete_all_rules(rules)
    set_rules(topic)
    topic_no_space = topic.replace(' ', '_')
    table_name = f"RawTweets-{topic_no_space}"
    create_landing_table(table_name=table_name)
    url = "https://api.twitter.com/2/tweets/search/stream"
    params = {
        'tweet.fields': ['created_at']
    }
    with requests.request("GET", url, headers=headers, stream=True, params=params) as response:
        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                print("running stream")
                print(f'json response: {json_response}')
                tweet = json_response["data"]
                index_tweet(tweet, table_name)
                logger.info(response_line)
                # print(tweet)