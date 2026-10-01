"""
메서드의 종류 : 메서드 자체의 코드는 동일하나 @데코레이터를 추가하여 성격을 정의함.
    1. 인스턴스 메서드 : 일반적인 형태의 메서드(클래스 내 함수)
    2. 정적 메서드 : 다른 메서드나 속성을 사용할 수 없는 메서드
    3. 클래스 메서드 : 다른 인스턴스 메서드를 호출 할 수 없는 메서드, 인스턴스 생성없이 사용이 가능
    4. 읽기 전용 속성 : 형식적으로는 메서드
"""


# 1. static method (정적 메서드), instance method (인스턴스 메서드)
class MyClass:
    classVal= "클래스 변수"
    
    def __init__(self,len,color):
        self._len = len
        self._color = color
    @staticmethod
    def staticMethod():
        print("정적 메서드 호출")
        
    
    def instanceMethod(self):
        self.staticMethod()

    @classmethod
    def testMethod(self):
        print("테스트 메서드 호출")
        
    @property
    def propertyMethod(self):
        return self._color

obj=MyClass(10,"red")
obj.staticMethod()
obj.instanceMethod()
MyClass.testMethod()    # 인스턴스 메서드는 외부에서 호출 할 때 클래스명 다음에 올 수 없다.
obj.testMethod()
print(obj.propertyMethod)
