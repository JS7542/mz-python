import json, os, boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    secret_name = boto3.client('secretsmanager', region_name='eu-north-1')
    
    
    #
    response = secret_name.get_secret_value(SecretId="rds!db-a2085765-95c3-4a7d-8b0d-93a625dd3ea0")
    secret_obj = json.loads(response['SecretString'])
    password = secret_obj['password']
    
    return {
        'statusCode': 200,
        'body': response['SecretString']
    }