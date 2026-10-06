import json, os, boto3
from botocore.exceptions import ClientError

# S3 전체 기능 사용 : boto3.client('s3'[, region_name='eu-north-1'])
s3_client = boto3.client('s3', region_name='eu-north-1')

# s3 리소스 사용 : resource 객체를 사용하면 S3 버킷과 객체를 더 직관적으로 다룰 수 있음
# s3_resource = boto3.resource('s3', region_name='eu-north-1')
def lambda_handler(event, context):
    cors_headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    }
    try:
        # response = s3_client.list_buckets(
        #     MaxBuckets=10000,             # 조회할 최대 버킷 수
        #     ContinuationToken='string',   # 다음 페이지의 결과를 가져올 때 사용
        #     Prefix='string',              # 특정 접두사로 시작하는 버킷만 조회하고 싶을 때 사용
        #     BucketRegion='string'         # 특정 리전의 버킷만 조회하고 싶을 때 사용
        #     )
        
        # list_buckets() 메서드는 기본적으로 모든 리전의 버킷을 조회하지만, 이 경우 BucketRegion 의 경우는 제한을 둔 경우에만 적용됨
        # response = s3_client.list_buckets(BucketRegion='eu-north-1')
        response = s3_client.list_buckets()
        # buckets_names = [bucket['Name'] for bucket in response['Buckets']]
        # buckets_region = [bucket['BucketRegion'] for bucket in response['Buckets']]
        # bucket_creation_date = [bucket['CreationDate'] for bucket in response['Buckets']]
        buckets = []
        for bucket in response.get('Buckets', []):
            REGION = s3_client.get_bucket_location(Bucket=bucket['Name']).get('LocationConstraint')
            buckets.append(f"Bucket: {bucket['Name']} Region: {REGION} Creation Date: {bucket['CreationDate'].isoformat()}")
            
        return {
            'statusCode': 200,
            'body': json.dumps({
                "count": len(buckets),
                "buckets": buckets
            },ensure_ascii=False),
            'headers': cors_headers
        }
        
    except ClientError as e:
        print(f"Error listing buckets: {e}")
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        return {
            'statusCode': 400,
            'body': json.dumps({
                "error": str(e),
                "code": error_code,
                "message": error_message
            }, ensure_ascii=False),
            'headers': cors_headers
        }
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                "error": str(e),
            }, ensure_ascii=False),
            'headers': cors_headers
        }
