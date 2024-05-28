import os
import json
import boto3
from botocore.exceptions import ClientError

ses_client = boto3.client('ses')

def lambda_handler(event, context):
    try:
        records = event['Records']
        for record in records:
            body = record['body']
            # Parse the body as a JSON object
            body_obj = json.loads(body)
            message = body_obj.get('message', 'No message found')
            recipient = body_obj['recipient']
            authCode = body_obj['authCode']
            subject = "Your One-Time Passcode (OTP)"
            body_text = f"Your OTP is: {authCode}\n\nPlease do not share this OTP with anyone."
            body_html = f"""<html>
            <head></head>
            <body>
            <h3>Your OTP is: {authCode}</h3>
            <p>Use your code to login and do not share this OTP with anyone.</p>
            </body>
            </html>"""
            # Construct the email
            response = ses_client.send_email(
                Source="todoeks@outlook.com",
                Destination={
                    'ToAddresses': [
                        recipient,
                    ],
                },
                Message={
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': subject,
                    },
                    'Body': {
                        'Text': {
                            'Data': body_text,
                        },
                        'Html': {
                            'Data': body_html,
                        },
                    },
                }
            )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Email sent successfully', 'response': response})
        }

    except ClientError as e:
        print('Error sending email:', e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to send email', 'error': e.response['Error']['Message']})
        }
    
    except Exception as e:
        print('Error:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to send email', 'error': str(e)})
        }
