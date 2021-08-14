import boto3

twitter_message_group_id = "twitterLandingTable"
queue_name = "twitter_queue.fifo"


def publish_message(message, topic):
    client = boto3.client('sqs')
    queues = client.list_queues()['QueueUrls']
    queue_url = ''
    for _ in queues:
        if queue_name in _:
            queue_url = _
            break

    send_response = client.send_message(
        QueueUrl=queue_url,
        MessageBody=message,
        MessageGroupId=twitter_message_group_id,
        MessageDeduplicationId=topic.replace(' ', '_')
    )

    return send_response['MD5OfMessageBody']
