import json,os,boto3
import urllib.request


def send_slack_message(message):
    
    SLACK_WEBHOOK_URL = ""
    
    # message = "payload 메세지 테스트"
    if not SLACK_WEBHOOK_URL:
        return {
            'statusCode': 400,
            'body': json.dumps('Slack Webhook URL is not configured.')
        }
        
    payload = {
        "text": message
    }
    
    req = urllib.request.Request(
        SLACK_WEBHOOK_URL,                              # SLACK 의 웹훅 주소
        data = json.dumps(payload).encode("utf-8"),     # 저장할 데이터
        headers = {
            "Content-Type": "application/json"
        }
    )
    
    try:
        urllib.request.urlopen(req)                         # 슬랙으로 메시지 전송
        
        return {
            'statusCode': 200,
            'body': json.dumps('Test Message Send Successfully!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Failed to send message: {str(e)}')
        }
        


# ====================================================================
# Lambda 함수 핸들러
def lambda_handler(event, context):
    ec2_client = boto3.client("ec2")
    detail = event.get("detail", {})                    # 이벤트 페이로드에서 정보 반환
    user_identity = detail.get("userIdentity", {}).get("arn", "")      # 이벤트를 발생시킨 사용자 정보 반환
    
    # 중복 메세지 발송을 막기 위한 이중 이벤트 제어
    if "IANSecurityAutoRemediationRole" in user_identity:
        return
    
    req_params =  detail.get("requestParameters", {})
    group_id = req_params.get("groupId", "")
    
    nat_instance_group_id = ""   
    # nat instnace 관련 추가 로직
    # [적용 예외] group_id 활용
    if group_id == nat_instance_group_id:
        return
    
    
    ip_perms = req_params.get("ipPermissions", {})          # 보안 그룹 인바운드 규칙
    perms_list = ip_perms if isinstance(ip_perms,list) else ip_perms.get("items",[])
    
    for perm in perms_list:
        if perm.get("fromPort") == 22 or perm.get("toPort") == 22:
            ip_ranges = perm.get("ipRanges",[])
            ranges_list = ip_ranges if isinstance(ip_ranges,list) else ip_ranges.get("items",[])
            
            
            
            # 인바운드 규칙 삭제
            for r in ranges_list:
                if r.get("cidrIp") == "0.0.0.0/0":
                    ec2_client.revoke_security_group_ingress(
                        GroupId=group_id,
                        IpPermissions=[{
                            "IpProtocol": str(perm.get("ipProtocol" , "tcp")),
                            "FromPort": 22,
                            "ToPort": 22,
                            "IpRanges": [{
                                "CidrIp":  "0.0.0.0/0"
                            }]
                        }]
                            
                    )
    
                    # 슬랙에 전송할 메시지 설정
                    message = (
                        f"🚨 ## [보안 위협 자동 차단 완료] ## 🚨\n"
                        f"* 보안 그룹 ID : '{group_id}' *\n"
                        f"* 위반 작업자 : '{user_identity}' *\n"
                        f"* 위반 내용 : SSH(22) 포트 '{ip_perms}' 퍼블릭 오픈 *\n"
                        f"* 조치 사항 : 해당 Inbound Role 자동 삭제 처리됨 *"
                    )              
                    # 슬랙으로 메시지 전송
                    send_slack_message(message)                         
    
    