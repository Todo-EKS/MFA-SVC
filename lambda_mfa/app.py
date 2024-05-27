import json

def lambda_handler(event, context):

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Lambda MFA",
            # "location": ip.text.replace("\n", "")
        }),
    }
