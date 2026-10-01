# 클래스 상속
import os
class Parent:
    def __init__(self, a,b):
        self.a = a
        self.b = b
        
    def prt(self):
        print(f"Parent: a={self.a}, b={self.b}")
        
# 클래스의 상속: 클래스명(부모클래스명)
class Child(Parent):
    def test(self):
        print(f"Child: a={self.a}, b={self.b}")
        
    def prt(self):
        print(f"Child: a={self.a}, b={self.b}")
        
        
obj = Child(10,20)
obj.test()
obj.prt()

        
        
# class Calculator:
#     def __init__(self,str, num1, num2):
#         self.str = str
#         self.num1 = num1
#         self.num2 = num2
        
#     def calculate(self):
#         if self.str == "+":
#             return self.num1 + self.num2
#         elif self.str == "-":
#             return self.num1 - self.num2
#         elif self.str == "*":
#             return self.num1 * self.num2
#         elif self.str == "/":
#             return self.num1 / self.num2
#         else:
#             return "잘못된 연산자입니다."

# input_str = input("첫번째 계산기 (클래스 기반) 연산자를 입력하세요 (+, -, *, /): ")
# num1 = int(input("첫 번째 숫자를 입력하세요: "))
# num2 = int(input("두 번째 숫자를 입력하세요: "))
# cal = Calculator(input_str, num1, num2)
# print(cal.calculate())


# class Calculator2:
#     def __init__(self, num1, num2):
#         self.num1 = num1
#         self.num2 = num2
    
#     def add(self):
#         return self.num1 + self.num2

#     def subtract(self):
#         return self.num1 - self.num2

#     def multiply(self):
#         return self.num1 * self.num2

#     def divide(self):
#         if self.num2 != 0:
#             return self.num1 / self.num2
#         else:
#             return "0으로 나눌 수 없습니다."
        

# input_str2 = input("두번째 계산기 (클래스에서 연산만 기반)연산자를 입력하세요 (+, -, *, /): ")
# num1_2 = int(input("첫 번째 숫자를 입력하세요: "))
# num2_2 = int(input("두 번째 숫자를 입력하세요: "))
# cal2 = Calculator2(num1_2, num2_2)

# if input_str2 == "+":
#     print(cal2.add())
# elif input_str2 == "-":
#     print(cal2.subtract())
# elif input_str2 == "*":
#     print(cal2.multiply())
# elif input_str2 == "/":
#     print(cal2.divide())
# else:
#     print("잘못된 연산자입니다.")
        
        


# class Calculator3:
#     def __init__(self, num1, num2):
#         self.num1 = num1
#         self.num2 = num2

    

# class CalAdd(Calculator3):
#     def add(self):
#         return self.num1 + self.num2
    
# class CalSubtract(Calculator3):
#     def subtract(self):
#         return self.num1 - self.num2

# class CalMultiply(Calculator3):
#     def multiply(self):
#         return self.num1 * self.num2

# class CalDivide(Calculator3):
#     def divide(self):
#         if self.num2 != 0:
#             return self.num1 / self.num2
#         else:
#             return "0으로 나눌 수 없습니다."


# input_str3 = input("세번째 계산기 (상속 기반) 연산자를 입력하세요 (+, -, *, /): ")
# num1_3 = int(input("첫 번째 숫자를 입력하세요: "))
# num2_3 = int(input("두 번째 숫자를 입력하세요: "))

# if input_str3 == "+":
#     cal3 = CalAdd(num1_3, num2_3)
#     print(cal3.add())
# elif input_str3 == "-":
#     cal3 = CalSubtract(num1_3, num2_3)
#     print(cal3.subtract())
# elif input_str3 == "*":
#     cal3 = CalMultiply(num1_3, num2_3)
#     print(cal3.multiply())
# elif input_str3 == "/":
#     cal3 = CalDivide(num1_3, num2_3)
#     print(cal3.divide())
# else:
#     print("잘못된 연산자입니다.")