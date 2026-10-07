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
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json; charset=utf-8"
    }

    s3_client = boto3.client("s3", region_name="eu-north-1")

    params = event.get("queryStringParameters") or {}
    action = params.get("action", "read")

    # ============================================================
    # 1. S3 버킷 목록 조회
    # ?action=list-buckets
    # ============================================================
    if action == "list-buckets":
        try:
            response = s3_client.list_buckets()

            bucket_list = [
                bucket["Name"]
                for bucket in response.get("Buckets", [])
            ]

            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps(
                    {"buckets": bucket_list},
                    ensure_ascii=False
                )
            }

        except ClientError as e:
            return {
                "statusCode": 500,
                "headers": headers,
                "body": json.dumps(
                    {
                        "message": "버킷 목록 조회 실패",
                        "error": str(e)
                    },
                    ensure_ascii=False
                )
            }

    # ============================================================
    # 2. 선택한 버킷의 폴더 / 객체 목록 조회
    # ?action=list-objects&bucket=버킷명&dir=Root
    # ============================================================
    if action == "list-objects":
        bucket_name = params.get("bucket", "")
        dir_name = params.get("dir", "Root")

        if not bucket_name:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps(
                    {"message": "버킷을 선택해주세요."},
                    ensure_ascii=False
                )
            }

        if dir_name in ["/", "", "Root", "root"]:
            prefix = ""
        else:
            prefix = dir_name.strip("/") + "/"

        try:
            response = s3_client.list_objects_v2(
                Bucket=bucket_name,
                Prefix=prefix,
                Delimiter="/"
            )

            folder_list = []

            for item in response.get("CommonPrefixes", []):
                folder_prefix = item["Prefix"]
                folder_name = folder_prefix[len(prefix):].rstrip("/")

                folder_list.append({
                    "name": folder_name,
                    "prefix": folder_prefix
                })

            file_list = []

            for obj in response.get("Contents", []):
                key = obj["Key"]

                # 폴더 표현용 객체 제외
                if key == prefix or key.endswith("/"):
                    continue

                file_name = key[len(prefix):]

                file_list.append({
                    "name": file_name,
                    "key": key,
                    "size": obj["Size"],
                    "lastModified": obj["LastModified"].isoformat()
                })

            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps(
                    {
                        "bucket": bucket_name,
                        "prefix": prefix,
                        "folders": folder_list,
                        "files": file_list,
                        "folderCount": len(folder_list),
                        "fileCount": len(file_list)
                    },
                    ensure_ascii=False
                )
            }

        except ClientError as e:
            return {
                "statusCode": 500,
                "headers": headers,
                "body": json.dumps(
                    {
                        "message": "S3 객체 목록 조회 실패",
                        "bucket": bucket_name,
                        "prefix": prefix,
                        "error": str(e)
                    },
                    ensure_ascii=False
                )
            }

    # ============================================================
    # 3. 객체 내용 읽기
    # ?action=read&bucket=버킷명&dir=폴더&file=파일명
    # ============================================================
    bucket_name = params.get("bucket", "std20-s3-main-lambda")
    dir_name = params.get("dir", "Root")
    file_name = params.get("file", "")

    if not file_name:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps(
                {"message": "파일명을 입력해주세요."},
                ensure_ascii=False
            )
        }

    if dir_name in ["/", "", "Root", "root"]:
        object_key = file_name
    else:
        object_key = f"{dir_name.strip('/')}/{file_name}"

    try:
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=object_key
        )

        file_content = response["Body"].read().decode("utf-8")

        headers["Content-Type"] = "text/plain; charset=utf-8"

        return {
            "statusCode": 200,
            "headers": headers,
            "body": file_content
        }

    except UnicodeDecodeError:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps(
                {
                    "message": "텍스트 형식으로 읽을 수 없는 파일입니다.",
                    "bucket": bucket_name,
                    "key": object_key
                },
                ensure_ascii=False
            )
        }

    except ClientError as e:
        return {
            "statusCode": 404,
            "headers": headers,
            "body": json.dumps(
                {
                    "message": "파일 조회 실패",
                    "bucket": bucket_name,
                    "key": object_key,
                    "error": str(e)
                },
                ensure_ascii=False
            )
        }

# def lambda_handler(event, context):
#     # CORS 헤더 설정(HTML 호출시 필요)
#     headers = {
#         'Access-Control-Allow-Origin': '*',
#         'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
#         'Access-Control-Allow-Headers': 'Content-Type',
#         "Content-Type": "text/plain; charset=utf-8" 
#     }
    
#     s3_client = boto3.client('s3')
    
#     # 디렉토리에 접근하는지 파일에 바로 접근하는지의 여부에 따라 제어를 수행하여야 한다.
#     bucket_name = "std20-terraform-state-s3-bucket"
#     dir_name = "CI-CD-Terra-Stockholm"
#     file_name = "terraform.tfstate"
#     if dir_name in ["/", "","Root","root"]:
#         object_key = file_name
#     else:
#         object_key = f"{dir_name}/{file_name}"
        
        
#     response = s3_client.get_object(
#         Bucket=bucket_name, 
#         Key=object_key
#     )
    
#     file_content = response['Body'].read().decode('utf-8')
    
#     return {
#         'statusCode': 200,
#         'headers': headers,
#         'body': file_content
#     }