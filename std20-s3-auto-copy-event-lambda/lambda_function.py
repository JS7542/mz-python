import json, os, boto3, urllib.parse
from botocore.exceptions import ClientError
from datetime import datetime

def lambda_handler(event, context):
    s3_client = boto3.client("s3")
    
    
    # S3에 지정된 이벤트
    record = event["Records"][0]["s3"]
    bucket = record["bucket"]["name"]
    raw_key = record["object"]["key"]
    # url 코드값을 일반형으로 변경 : urllib.parse.unquote.unquote_plus("변경할 문자열")
    object_key = urllib.parse.unquote_plus(raw_key)
    file_name = os.path.basename(object_key)

    name, ext = os.path.splitext(file_name)

    backup_file_name = f"{name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}{ext}"
    
    # 받아온 값을 바탕으로 backup 디렉토리에 복사
    
    try:
        s3_client.copy_object(
            Bucket=bucket,
            CopySource={'Bucket': bucket, 'Key': object_key},
            Key=f"backup/{backup_file_name}"
        )
    except ClientError as e:
        print(f"Error copying object {object_key} to backup/{backup_file_name}: {e}")

