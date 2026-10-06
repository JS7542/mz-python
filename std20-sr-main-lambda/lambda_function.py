import json, os, boto3, base64
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    s3 = boto3.client('s3', region_name='eu-north-1')
    
    # S3 버킷 이름 설정
    bucket_name = "std20-lambda-create-bucket-7830"
    
    # S3 버킷의 객체 목록 가져오기(조회)
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix='std20-file/', Delimiter='/')

    
    # 객체 키(파일명) 목록 추출(버킷이 비어있으면 Contents 키가 없음)
    # 즉, response가 'Contents' 라는 것은 버킷에 객체가 존재한다는 의미이다.
    file_list = []
    folder_list = []
    if "Contents" in response:
        file_list = [obj["Key"] for obj in response["Contents"] if not obj["Key"].endswith('/')]
        
    
    if "CommonPrefixes" in response:
        # CommonPrefixes 에서 Prefix 키 값을 로드
        folder_list = [prefix["Prefix"] for prefix in response["CommonPrefixes"]]
    
    result = {
        "files": file_list,
        "folders": folder_list
    }
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }