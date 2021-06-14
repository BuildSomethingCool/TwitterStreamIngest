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


def set_rule(topic):
    rule = {
        "add": [
            {
                "value": f"{topic} -has:media",
                "tag": f"{topic} without media"
            }
        ]
    }
    response = requests.request("POST", rules_endpoint, headers=headers, data=json.dumps(rule))
    return response.status_code


def get_all_rules():
    rules = []
    print(f"headers: {headers}")
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
    response = requests.request("POST", rules_endpoint, headers=headers, data=json.dumps(rule))
    return response.status_code


def connect_to_stream_and_ingest(topic):
    clear_existing_rules()
    set_rule(topic)
    topic_no_space = topic.replace(' ', '_')
    table_name = f"RawTweets-{topic_no_space}"
    create_landing_table(table_name=table_name)
    url = "https://api.twitter.com/2/tweets/search/stream"
    params = {
        'tweet.fields': ['created_at']
    }
    response = requests.request("GET", url, headers=headers, stream=True, params=params)
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print("running stream")
            print(f'json response: {json_response}')
            tweet = json_response["data"]
            index_tweet(tweet, table_name)
            logger.info(response_line)
            # print(tweet)