import json
import boto3
from botocore.exceptions import ClientError

s3 = boto3.resource('s3', region_name='eu-north-1')
s3_client = boto3.client('s3', region_name='eu-north-1')

CORS_HEADERS = {
    'Content-Type': 'application/json; charset=utf-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'DELETE, OPTIONS',
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

    query_params = event.get('queryStringParameters') or {}
    bucket_name = (query_params.get('bucket_name') or '').strip()

    if not bucket_name:
        return response(400, {
            'deleted': False,
            'reason': '삭제할 bucket_name이 전달되지 않았습니다.'
        })

    try:
        # 버킷 존재 및 접근 가능 여부 확인
        s3_client.head_bucket(Bucket=bucket_name)

        bucket = s3.Bucket(bucket_name)

        # 버전이 있는 객체, Delete Marker, 일반 객체까지 정리
        bucket.object_versions.delete()

        # 버킷 삭제
        bucket.delete()

        return response(200, {
            'bucket_name': bucket_name,
            'deleted': True,
            'reason': '버킷과 내부 객체 삭제 성공'
        })

    except ClientError as e:
        error_code = str(e.response['Error']['Code'])
        error_message = e.response['Error']['Message']

        if error_code == '404' or error_code == 'NoSuchBucket':
            reason = '삭제할 버킷이 존재하지 않습니다.'
            status_code = 404

        elif error_code == '403' or error_code == 'AccessDenied':
            reason = '버킷 삭제 권한이 없거나 해당 버킷에 접근할 수 없습니다.'
            status_code = 403

        elif error_code == 'BucketNotEmpty':
            reason = '버킷 내부에 삭제되지 않은 객체 또는 버전이 남아 있습니다.'
            status_code = 409

        else:
            reason = '버킷 삭제 중 오류가 발생했습니다.'
            status_code = 400

        return response(status_code, {
            'bucket_name': bucket_name,
            'deleted': False,
            'reason': reason,
            'error_code': error_code,
            'error_message': error_message
        })

    except Exception as e:
        return response(500, {
            'bucket_name': bucket_name,
            'deleted': False,
            'reason': '예상하지 못한 시스템 오류가 발생했습니다.',
            'error': str(e)
        })
