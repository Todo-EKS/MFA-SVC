import os
import json
import boto3

def lambda_handler(event, context):
    # Create SQS client
    sqs = boto3.client('sqs')
    
     # Access environment variables
    queue_url = os.environ['QUEUE_URL']

    # Receive message from SQS queue
    sqs_trigger_response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'All'
        ],
        MaxNumberOfMessages=1,
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
   
    # Check if messages are received
    if 'Messages' in sqs_trigger_response:
        for message in sqs_trigger_response['Messages']:
            # Print message body to console
            print("Received message:", message['Body'])
            
            # Delete the message from the queue
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
    else:
        print("No messages in the queue")

    return {
        'statusCode': 200,
        'body': 'Messages processed successfully'
    }
