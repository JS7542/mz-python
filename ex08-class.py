# ========================================================
# 기본 클래스 구조
# 보통 클래스는 첫 시작이 대문자
# ========================================================
import os
class MyClass:
    # ----------------------------------------------------
    # 클래스 변수
    # 어느곳에서나 <클래스명.클래스변수>로 접근 가능
    class_var = 100
    # 인스턴스 변수
    # 인스턴스마다 별도로 존재하며, <인스턴스명.인스턴스변수>로 접근 가능
    # 클래스 내에서는 <self.인스턴스변수>로 접근 가능
    
    # ----------------------------------------------------
    
    # __init__(self)  메서드는 초기화 메서드로
    # 클래스 초기화 설정에 사용되며, 인스턴스 생성할때, 맨 처음으로 자동 실행
    # 필수는 아니지만, 일부로 사용하지않는 이상 실무에서는 대게 사용됨
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.result = x + y
        
    def prtMeth(self,x=0,y=0):
        print(f"This is a method in MyClass: x={x}, y={y}, class_var={MyClass.class_var}")
        
    def chgClassVar(self, value):
        MyClass.class_var += value
        
        return MyClass.class_var
        
     
os.system("clear")

obj1 = MyClass(10,20)
obj2 = MyClass(100,200)

obj1.prtMeth(10,20)
print(f"MyClass.class_var before change: {MyClass.class_var}")
print(obj1.chgClassVar(50))
print(f"MyClass.class_var after change: {MyClass.class_var}")
obj1.prtMeth(10,20)

os.system("clear")

print(f"obj1: x={obj1.x}, y={obj1.y}, result={obj1.result}")
print(f"obj2: x={obj2.x}, y={obj2.y}, result={obj2.result}")

