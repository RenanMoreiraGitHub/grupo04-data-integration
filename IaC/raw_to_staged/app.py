import json

def lambda_handler(event, context):
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        print(f"Received a new object in bucket '{bucket_name}': '{object_key}'")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Raw to Staged Lambda executed successfully!')
    }
