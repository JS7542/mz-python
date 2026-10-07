import json
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json; charset=utf-8"
    }

    # ============================================================
    # OPTIONS 요청 처리
    # ============================================================
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": ""
        }

    # ============================================================
    # 클라이언트 데이터
    # ============================================================
    body = json.loads(event.get("body", "{}"))

    bucket = body.get("bucket")
    dir_path = body.get("dir_path", "/")
    file_name = body.get("file_name")
    file_type = body.get(
        "file_type",
        "application/octet-stream"
    )

    if not bucket:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({
                "message": "버킷이 지정되지 않았습니다."
            })
        }

    if not file_name:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({
                "message": "파일명이 지정되지 않았습니다."
            })
        }

    # ============================================================
    # S3 Object Key
    # ============================================================
    if dir_path in ["root", "Root", "", "/"]:
        object_key = file_name
    else:
        clean_dir_path = dir_path.strip("/")
        object_key = f"{clean_dir_path}/{file_name}"

    # ============================================================
    # Presigned URL 생성
    # ============================================================
    s3_client = boto3.client(
        "s3",
        region_name="eu-north-1"
    )

    try:
        presigned_url = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": bucket,
                "Key": object_key,
                "ContentType": file_type
            },
            ExpiresIn=300
        )

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "presigned_url": presigned_url,
                "bucket": bucket,
                "key": object_key
            })
        }

    except ClientError as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({
                "message": "Presigned URL 생성 실패",
                "error": str(e)
            })
        }

# import json, os, boto3
# from botocore.exceptions import ClientError



# def lambda_handler(event, context):
#     headers = {
#         "Access-Control-Allow-Origin": "*",
#         "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
#         "Access-Control-Allow-Headers": "Content-Type",
#         "Content-Type": "application/json; charset=utf-8"
#     }
#     # ========================================================
#     # 클라이언트로부터 전송되어온 데이터 변수화
#     body = json.loads(event.get("body", "{}"))
#     bucket = body.get("bucket")
#     dir_path = body.get("dir_path","/")
#     file_name = body.get("file_name")
#     file_type = body.get("file_type", "application/octet-stream")

#     if dir_path in ["root","Root", "", "/"]:
#         object_key = file_name
#     else:
#         clean_dir_path = dir_path.strip("/")
#         object_key = f"{clean_dir_path}/{file_name}"
#     #=========================================================
    
#     s3_client = boto3.client("s3")

#     # 클라이언트가 S3 로 직접 파일을 PUT 전송 할 수 있는 presigned URL 생성
#     presigned_url = s3_client.generate_presigned_url(
#         ClientMethod="put_object",
#         Params={
#             "Bucket": bucket,
#             "Key": object_key,
#             "ContentType": file_type                                  # 업로드 할 파일의 유형 (클라이언트의 PUT 요청)
#         },
#         ExpiresIn=300
#     )

#     return {
#         "statusCode": 200,
#         "headers": headers,
#         "body": json.dumps({"presigned_url": presigned_url})
#     }