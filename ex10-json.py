# JSON 자료형의 형 변환
# json.loads() : JSON 형식의 문자열 데이터를 JSON 타입(Python 객체)으로 변환
# json.dumps() : Python 객체를 JSON 문자열로 변환

import json

str ="""["홍길동","100","90","80"]"""
json_data = json.loads(str)
print(type(json_data),json_data[0])

data = json.dumps(json_data, ensure_ascii=False)
print(type(data),data)

