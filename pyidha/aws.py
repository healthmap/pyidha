import os
import json
import time
import boto3
from botocore.exceptions import ClientError
from pyidha.utils import create_chunks


def create_cross_account_client(role, session_name, service):
    """Creates a client object that gives access to a different account.

    Parameters
    __________
    role : str
        Full arn for role in account. Must have permission to assume.
        Format: "arn:aws:iam::account-of-role-to-assume:role/name-of-role"
    session_name : str
        Name for temporary session.
    service : str
        Service name for client desired, e.g. "s3"

    Returns
    _______
    object
        Client object configured with credentials for cross-account
        access.
    """
    sts_client = boto3.client("sts")

    assumed_role_object = sts_client.assume_role(
        RoleArn=role, RoleSessionName=session_name
    )

    credentials = assumed_role_object["Credentials"]

    # Use the temporary credentials that AssumeRole returns to make a
    # connection to Amazon S3
    cross_account_client = boto3.client(
        service,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )

    return cross_account_client


def enqueue_message(queue_url, message):
    """Sends message to AWS queue.

    Parameters
    __________
    queue_url : str
        URL for SQS queue.
    message : dict

    """
    aws_region = os.environ.get("AWS_REGION")
    client = boto3.client("sqs", region_name=aws_region)

    try:
        response = client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message),
        )
        print(response)
        return response
    except ClientError as e:
        print(e.response["Error"]["Message"])
        print(message)
        raise ClientError("Message failed to enqueue and will not be sent.")


def enqueue_messages(queue_url, messages):
    """Sends emails to recipients using settings.

    Parameters
    __________
    queue_url : str
        URL for SQS queue.
    messages : list of dict

    """
    client = boto3.client("sqs")
    try:
        responses = []
        start_time = time.time()
        message_chunks = create_chunks(messages, 10)
        for chunk in message_chunks:
            response = client.send_message_batch(QueueUrl=queue_url, Entries=chunk)
            responses.append(response)
            print(response)
        elapsed_time = time.time() - start_time
        print(f"Message processed in {elapsed_time} seconds.")
        return responses
    except ClientError as e:
        print(e.response["Error"]["Message"])
        print(messages)
        raise ClientError("Messages failed to enqueue and will not be sent.")


def delete_message(queue_url, message):
    """Deletes a message from a queue.

    Parameters
    __________
    queue_url : str
        URL for SQS queue.
    message : dict
        message metadata, must contain ReceiptHandle

    Returns
    _______
    response : dict
        Result of API call.

    """
    aws_region = os.environ.get("AWS_REGION")
    client = boto3.client("sqs", region_name=aws_region)
    try:
        response = client.delete_message(
            QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"]
        )
    except ClientError as e:
        print(e.response["Error"]["Message"])
        raise ClientError("Message deletion failed.")
    return response


def delete_messages(queue_url, receipt_handles):
    """Deletes messages from a queue.

    Parameters
    __________
    queue_url : str
        URL for SQS queue.
    receipt_handles : list
        Message ids for deletion.

    """
    client = boto3.client("sqs")
    try:
        responses = []
        start_time = time.time()
        message_chunks = create_chunks(receipt_handles, 10)
        for chunk in message_chunks:
            response = client.delete_message_batch(QueueUrl=queue_url, Entries=chunk)
            responses.append(response)
            print(response)
        elapsed_time = time.time() - start_time
        print(f"Message processed in {elapsed_time} seconds.")
        return responses
    except ClientError as e:
        print(e.response["Error"]["Message"])
        print(receipt_handles)
        raise ClientError("Messages failed to enqueue and will not be sent.")
