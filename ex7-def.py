# 함수 생성 기본 구성 (형식)
"""
def 함수명(변수1, 변수2, 변수3):
    실행할 코드
        :
    [return 반환값]
"""

# 함수 호출
# [변수 = ]함수명(값1, 값2, 값3)
# 권장 방식: true, false 등 뭐라도 리턴 시켜서 함수가 정상 작동 하는지, 정상 종료 하였는지 확인
import os

os.system('clear')
# def funAdd(fir, sec=0):
#     return fir + sec

# print(funAdd(4,))


def basicFactorial(n):
    if n == 1:
        return 1
    else:
        return n * basicFactorial(n - 1)
    

print(basicFactorial(5))

def tailFactorial(n, total):
    print(n)
    if n == 1:
        return total
    else:
        return tailFactorial(n - 1, n * total)

print(tailFactorial(3, 3))

# ===============================
# 대표적인 쓰임세
def convInt():
    data = input("숫자를 입력하세요: ")
    try:
        return int(data)
    except :
        print("유효한 숫자가 아닙니다.")
        convInt()
        
print(convInt())