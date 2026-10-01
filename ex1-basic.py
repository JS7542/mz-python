"""
Basic example script for Python.
"""

a = 2
for i in range(2,5):
    print(a, "x",i, "=", a*i)
    print("---------------------")
    
print("##########################")


# 출력문 print() 사용하기

# %s : 문자열을 출력할 때 사용
# %d : 정수를 출력할 때 사용
# %f : 실수를 출력할 때 사용

print("A값 출력")
name = "홍길동"
Name = "이순신"
이름 = "김철수"
print(f"{이름} {name} {Name}")
print("이름 :%1s" % (name))
print("이름 :%s" % (Name))
print("이름 :%s" % (이름))

print("%2s :%5d \t%3s%5.1f" % ("정수", 123,"실수:" ,13.16))
print("a={1}, b={1} ".format(a, a))