import json, os, boto3
from botocore.exceptions import ClientError


s3_resource = boto3.resource('s3')

def lambda_handler(event, context):
    
    try:
        s3_resource.meta.client.head_bucket(Bucket="kso-bucket", ExpectedBucketOwner="925047940866")
        exists = True
    except ClientError as e:
        exists = False
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        if error_code == '404':
            error_message = 'Bucket does not exist'
        elif error_code == '403':
            error_message = 'Access to the bucket is forbidden'
        else:
            error_message = 'An unexpected error occurred'
        return {
            'statusCode': 400,
            'body': json.dumps({
                "exists": exists,
                "error": str(e),
                "code": error_code,
                "message": error_message
            }, ensure_ascii=False)
        }

    # 버킷의 존재 유무 및 권한 확인 후 추가 실행문 작성 (exists , error_code)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            "exists": exists,
            "message": 'Bucket exists and is accessible'
        }, ensure_ascii=False)
    }