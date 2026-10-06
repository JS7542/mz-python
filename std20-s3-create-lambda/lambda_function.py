import json
import boto3
import random
import re
from botocore.exceptions import ClientError

s3 = boto3.client('s3', region_name='eu-north-1')

REGION = 'eu-north-1'

CORS_HEADERS = {
    'Content-Type': 'application/json; charset=utf-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
}


def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': CORS_HEADERS,
        'body': json.dumps(body, ensure_ascii=False)
    }


def lambda_handler(event, context):
    method = (
        event.get('requestContext', {})
             .get('http', {})
             .get('method', '')
             .upper()
    )

    if method == 'OPTIONS':
        return response(200, {'message': 'OK'})

    try:
        body = event.get('body') or '{}'

        if isinstance(body, str):
            body = json.loads(body)

        requested_name = (body.get('bucket_name') or '').strip()

        if requested_name:
            bucket_name = requested_name
        else:
            rand_num = random.randint(0, 9999)
            bucket_name = f"std20-lambda-create-bucket-{rand_num:04d}"

        # 기본적인 버킷 이름 형식 검증
        if not re.fullmatch(r'[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]', bucket_name):
            return response(400, {
                'bucket_name': bucket_name,
                'created': False,
                'reason': 'S3 버킷 이름 형식이 올바르지 않습니다.'
            })

        # 1. 버킷 존재 여부 확인
        try:
            s3.head_bucket(Bucket=bucket_name)

            return response(409, {
                'bucket_name': bucket_name,
                'created': False,
                'reason': '이미 존재하며 현재 계정에서 접근 가능한 버킷입니다.'
            })

        except ClientError as e:
            error_code = str(e.response['Error']['Code'])
            error_message = e.response['Error']['Message']

            if error_code == '404':
                pass
            elif error_code == '403':
                return response(409, {
                    'bucket_name': bucket_name,
                    'created': False,
                    'reason': '해당 버킷 이름이 이미 사용 중이거나 접근 권한이 없습니다.',
                    'error_code': error_code,
                    'error_message': error_message
                })
            else:
                return response(500, {
                    'bucket_name': bucket_name,
                    'created': False,
                    'reason': '버킷 존재 여부를 확인하는 과정에서 오류가 발생했습니다.',
                    'error_code': error_code,
                    'error_message': error_message
                })

        # 2. 버킷 생성
        try:
            if REGION == 'us-east-1':
                s3.create_bucket(Bucket=bucket_name)
            else:
                s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': REGION
                    }
                )

            return response(200, {
                'bucket_name': bucket_name,
                'region': REGION,
                'created': True,
                'reason': '버킷 생성 성공'
            })

        except ClientError as e:
            error_code = str(e.response['Error']['Code'])
            error_message = e.response['Error']['Message']

            reasons = {
                'BucketAlreadyExists': '해당 버킷 이름이 다른 AWS 계정에서 이미 사용 중입니다.',
                'BucketAlreadyOwnedByYou': '해당 버킷이 이미 현재 AWS 계정에 존재합니다.',
                'AccessDenied': 'Lambda 실행 역할에 S3 버킷 생성 권한이 없습니다.',
                'InvalidBucketName': 'S3 버킷 이름 규칙에 맞지 않는 이름입니다.',
                'TooManyBuckets': 'AWS 계정의 S3 버킷 생성 한도에 도달했습니다.',
                'InvalidLocationConstraint': '지정한 S3 리전 설정이 올바르지 않습니다.'
            }

            return response(400, {
                'bucket_name': bucket_name,
                'region': REGION,
                'created': False,
                'reason': reasons.get(
                    error_code,
                    'S3 버킷 생성 중 예상하지 못한 오류가 발생했습니다.'
                ),
                'error_code': error_code,
                'error_message': error_message
            })

    except Exception as e:
        return response(500, {
            'created': False,
            'reason': '예상하지 못한 시스템 오류가 발생했습니다.',
            'error': str(e)
        })
