import json, os, boto3
from botocore.exceptions import ClientError
"""
# ===============================================================================================================

1. 객체 조회 및 다운로드
    <객체 변수> = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    <변수> = <객체 변수>['Body'].read().decode('utf-8')

2. 객체 목록 조회
    <객체 목록> = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=dir_name)
    <변수> = [obj['Key'] for obj in <객체 목록>.get('Contents', [])]
    
3. 객체 삭제
    s3_client.delete_object(Bucket=bucket_name, Key=object_key)
    
4. 다중 객체 삭제
    s3_client.delete_objects(
        Bucket=bucket_name,
        Delete={
            'Objects': [
                {'Key': obj_key} for obj_key in <객체 목록>
            ],
            'Quiet': True   # 기본값 False , True로 설정할 경우 오류가 발생한 객체에 대한 응답 반환
        }
    )

5. 객체 복사
    s3_client.copy_object(
        Bucket = destination_bucket_name,   # 복사본이 저장될 버킷 이름
        Key = destination_object_key,       # 복사본의 객체 키
        CopySource = {
            'Bucket': source_bucket_name,   # 원본 객체가 저장된 버킷 이름
            'Key': source_object_key        # 원본 객체의 키
        }
    )
    
    
# ===============================================================================================================
"""

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'text/plain; charset=utf-8'
    }

    s3_client = boto3.client('s3', region_name='eu-north-1')
    params = event.get("queryStringParameters") or {}
    
    bucket_name = params.get(
        "bucket",
        "std20-s3-main-lambda"
    )

    dir_name = params.get(
        "dir",
        "Root"
    )

    file_name = params.get(
        "file",
        ""
    )

    if not file_name:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': '삭제할 파일명을 입력해주세요.'
        }

    if dir_name in ["/", "", "Root", "root"]:
        object_key = file_name
    else:
        object_key = f"{dir_name.strip('/')}/{file_name}"

    try:
        s3_client.delete_object(
            Bucket=bucket_name,
            Key=object_key
        )

        return {
            'statusCode': 200,
            'headers': headers,
            'body': f"삭제 완료\n\n"
                    f"Bucket: {bucket_name}\n"
                    f"Key: {object_key}"
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': f"삭제 실패\n\n{str(e)}"
        }
        


# def lambda_handler(event, context):
#     # CORS 헤더 설정(HTML 호출시 필요)
#     headers = {
#         'Access-Control-Allow-Origin': '*',
#         'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
#         'Access-Control-Allow-Headers': 'Content-Type',
#         "Content-Type": "text/plain; charset=utf-8" 
#     }
    
# # ============================================================

# # ============================================================
# # 단일 객체 삭제 
#     # s3_client = boto3.client('s3')
#     # bucket_name = "std20-s3-main-lambda"
#     # dir_name = "/"
#     # file_name = "lambda_function_copy.py"

#     # if dir_name in ["/", "","Root","root"]:
#     #     object_key = file_name
#     # else:
#     #     object_key = f"{dir_name}/{file_name}"

#     # s3_client.delete_object(Bucket=bucket_name, Key=object_key)


#     # return {
#     #     'statusCode': 200,
#     #     'headers': headers,
#     #     'body': f"Deleted {object_key} from {bucket_name}" if object_key else f"Deleted {file_name} from {bucket_name}"
#     # }

# # ============================================================

# # ============================================================
# # 다중 객체 삭제
#     s3_client = boto3.client('s3')
#     bucket_name = "std20-s3-main-lambda"
#     delete_files = ["lambda_function_copy.py","lambda_function_copy2.py"]
#     dir_name = "/"
#     object_keys = []
#     for file_name in delete_files:
#         if dir_name in ["/", "","Root","root"]:
#             object_keys.append(file_name)
#         else:
#             object_keys.append(f"{dir_name}/{file_name}")

#     if delete_files:
#         s3_client.delete_objects(
#             Bucket=bucket_name,
#             Delete={
#                 'Objects' :[
#                     {'Key': object_key} for object_key in object_keys
#                 ],
#                 'Quiet': True
#             }
#         )

#     return{
#         'statusCode': 200,
#         'headers': headers,
#         'body': f"Deleted {', '.join(object_keys)} from {bucket_name}" if object_keys else f"No files deleted from {bucket_name}"
#     }

# # ============================================================