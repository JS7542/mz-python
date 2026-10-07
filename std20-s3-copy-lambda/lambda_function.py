import json, os, boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'text/plain; charset=utf-8'
    }

    s3_client = boto3.client('s3', region_name='eu-north-1')

    params = event.get("queryStringParameters") or {}

    # ========================================================
    # 원본
    # ========================================================

    source_bucket_name = params.get(
        "bucket",
        "std20-s3-main-lambda"
    )

    source_dir_name = params.get(
        "dir",
        "Root"
    )

    source_file_name = params.get(
        "file",
        ""
    )

    # ========================================================
    # 복사 목적지
    # ========================================================

    destination_bucket_name = params.get(
        "dest_bucket",
        source_bucket_name
    )

    destination_dir_name = params.get(
        "dest_dir",
        "Root"
    )

    destination_file_name = params.get(
        "dest_file",
        source_file_name
    )

    if not source_file_name:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': '원본 파일명을 입력해주세요.'
        }

    if not destination_file_name:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': '복사할 파일명을 입력해주세요.'
        }

    # 원본 Key
    if source_dir_name in ["/", "", "Root", "root"]:
        source_object_key = source_file_name
    else:
        source_object_key = (
            f"{source_dir_name.strip('/')}/{source_file_name}"
        )

    # 목적지 Key
    if destination_dir_name in ["/", "", "Root", "root"]:
        destination_object_key = destination_file_name
    else:
        destination_object_key = (
            f"{destination_dir_name.strip('/')}/"
            f"{destination_file_name}"
        )

    try:
        s3_client.copy_object(
            Bucket=destination_bucket_name,
            Key=destination_object_key,
            CopySource={
                'Bucket': source_bucket_name,
                'Key': source_object_key
            }
        )

        return {
            'statusCode': 200,
            'headers': headers,
            'body':
                f"복사 완료\n\n"
                f"원본\n"
                f"Bucket: {source_bucket_name}\n"
                f"Key: {source_object_key}\n\n"
                f"복사본\n"
                f"Bucket: {destination_bucket_name}\n"
                f"Key: {destination_object_key}"
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': f"복사 실패\n\n{str(e)}"
        }
# def lambda_handler(event, context):
#     # CORS 헤더 설정(HTML 호출시 필요)
#     headers = {
#         'Access-Control-Allow-Origin': '*',
#         'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
#         'Access-Control-Allow-Headers': 'Content-Type',
#         "Content-Type": "text/plain; charset=utf-8" 
#     }
    
 
# # 파일 복사 ============================================
#     s3_client = boto3.client('s3')
#     bucket_name = "std20-s3-main-lambda"
#     dir_name = "07.30"
#     file_name = "lambda_function_copy3.py"
#     source_bucket_name = "std20-s3-main-lambda"
#     source_dir_name = "07.15"
#     source_file_name = "lambda_function.py"
    
#     if dir_name in ["/", "","Root","root"]:
#         object_key = file_name
#     else:
#         object_key = f"{dir_name}/{file_name}"
    
#     if source_dir_name in ["/", "","Root","root"]:
#         source_object_key = source_file_name
#     else:
#         source_object_key = f"{source_dir_name}/{source_file_name}"
        
#     s3_client.copy_object(
#         Bucket=bucket_name,
#         Key=object_key,
#         CopySource={
#             'Bucket': source_bucket_name,
#             'Key': source_object_key
#         }
#     )

#     return {
#         'statusCode': 200,
#         'headers': headers,
#         'body': f"Copied {object_key} in {bucket_name}" if object_key else f"Copied {file_name} in {bucket_name}"
#     }