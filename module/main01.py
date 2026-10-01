# 모듈 호출부
# # 1. 일반적인 모듈 호출
# import module_sample
# calc = module_sample.ClassParent(10, 20)

# # 2. 별칭 사용
# import module_sample as ms
# calc = ms.ClassParent(10,20)


# 3. 클래스 사용 예제
# from module_sample import ClassParent
# calc = ClassParent(10, 20)

import test.module_sample as module_sample
calc = module_sample.ClassChild(10, 20)
res=calc.fumnAdd()
print(f"결과값: {res}")

res=calc.fumnSubtract()
print(f"결과값: {res}")

res=calc.fumnMultiply()
print(f"결과값: {res}")

res=calc.fumnDivide()
print(f"결과값: {res}")

print(calc.__doc__)
print(calc.add.__doc__)
print(calc.subtract.__doc__)
print(calc.multiply.__doc__)
print(calc.divide.__doc__)
