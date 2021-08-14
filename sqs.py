import boto3

twitter_message_group_id = "twitterLandingTable"
queue_name = "twitter_queue.fifo"


def publish_message(message, topic):
    client = boto3.client('sqs')
    queue_url = client.get_queue_url(
        QueueName=queue_name
    )['QueueUrl']

    send_response = client.send_message(
        QueueUrl=queue_url,
        MessageBody=message,
        MessageGroupId=twitter_message_group_id,
        MessageDeduplicationId=topic
    )

    return send_response['MD5OfMessageBody']
