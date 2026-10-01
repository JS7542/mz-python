import os
# 딕셔너리의 기본 구조
"""
    {"key1": "value1", "key2": "value2", "key3": "value3"}
    {
        'key1' : {'key1' : 'value1', 'key2' : 'value2'},
        'key2' : {'key1' : 'value1', 'key2' : 'value2'}
                            :
        'key3' : {'key1' : 'value1', 'key2' : 'value2'}
        
    }

"""
# Dict 선언 : 변수 = {}, 또는 변수 = dict()

os.system("clear")
print("="*30)
my_dict = {}  # 빈 딕셔너리 선언
my_dict2 = dict()  # 빈 딕셔너리 선언

# 초기값 지정 방법
my_dict = {
    "name" : ["길동", "철수", "영희"],
    "location" : ["서울", "부산", "대구"],
    "part" : ["개발", "디자인", "기획"]
    
}  # 초기값 지정

# 실무 패턴
# my_list = [
#     {"name" : "길동", "location" : "서울", "part" : "개발"},
#     {"name" : "철수", "location" : "부산", "part" : "디자인"},
#     {"name" : "영희", "location" : "대구", "part" : "기획"}
# ]

print(my_dict["name"][0])
# ==================================================================
os.system("clear")
print("="*30)

my_dict = {1: "길동", 2: "철수"}

print(my_dict[1])

os.system("clear")
print("="*30)
#  딕셔너리 메서드
"""
get() : 키에 해당하는 값을 반환하며, 키가 없으면 None을 반환합니다.
update() : 딕셔너리를 병합합니다.
keys() : 딕셔너리의 모든 키를 반환합니다.
values() : 딕셔너리의 모든 값을 반환합니다.
items() : 딕셔너리의 모든 키-값 쌍을 반환합니다.
pop() : 키에 해당하는 값을 제거하고 반환합니다.
clear() : 딕셔너리의 모든 항목을 제거합니다.
setdefault() : 키가 딕셔너리에 없으면 키와 값을 추가하고, 키에 해당하는 값을 반환합니다.
popitem() : 임의의 키-값 쌍을 제거하고 반환합니다.

"""


"""
    ==데이터 추가==
- get(key) : 키에 해당하는 값을 반환, 키가 없으면 None 반환
    val = 딕셔너리.get(key)
    
- update(key, value) : 딕셔너리를 병합합니다.
    딕셔너리.update({key: value})
"""
my_dict[3] = "영희"
print(my_dict.get(3))

my_dict.update({4: "민수"})
print(my_dict[4])

