import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb", region_name='ap-northeast-1')
table = dynamodb.Table('customer')


def lambda_handler(event, context):
    try:
        http_method = event.get("httpMethod")
        # Add CORS in response header
        responseHeader = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # Replace with your domain for production
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        }

        responseBody = {}
        # Process GET method
        if http_method == "GET":
            # Read query parameter
            customerId = event.get("queryStringParameters", {}).get(
                "CustomerId", "No Value"
            )

            resultSet = table.get_item(
                Key={'CustomerId': customerId})
            dataSet = resultSet["Item"]
            responseBody = [
                {'CustomerId': dataSet['CustomerId'], 'Name': dataSet['Name'], 'Email': dataSet['Email']}]

            print('Data Retrieved...')
            print(responseBody)

            return {
                "statusCode": 200,
                "headers": responseHeader,
                "body": json.dumps({"message": responseBody})
            }

        # Process POST method
        elif http_method == 'POST':
            # Parse request body
            body = json.loads(event['body'])
            print('Request Payload... ')
            print(body)
            id = body.get('id')
            name = body.get('name')
            email = body.get('email')
            if not id or not name or not email:
                return {
                    "statusCode": 400,
                    "headers": responseHeader,
                    "body": json.dumps({"error": "CustomerId, Name,Email Required."})
                }

            # Insert item into DynamoDB
            table.put_item(Item={"CustomerId": id, "Name": name, "Email": email})
            return {
                "statusCode": 200,
                "headers": responseHeader,
                "body": json.dumps({"message": "1 Item Inserted successfully!"})
            }
        else:
            return {
                "statusCode": 405,
                "headers": responseHeader,
                "body": json.dumps({"error": "Invalid Request Method "})
            }

    except ClientError as e:
        return {
            "statusCode": 500,
            "headers": responseHeader,
            "body": json.dumps({"error": str(e)})
        }
