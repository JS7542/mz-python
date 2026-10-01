#모듈 해더
"""
모듈명 : 사칙연산 모듈
작성자 : 윤진수
작성일 : 2026-10-01
"""

class ClassParent:
    """
    ClassParent 클래스는 사칙연산의 기본 기능을 제공하는 부모 클래스입니다.
    add
    subtract
    multiply
    divide
    """
    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b
        self.result = 0
    def add(self):
        """
        두 수의 합을 반환합니다.
        Args:
            self.a (int, optional): 첫 번째 숫자. 기본값은 0입니다.
            self.b (int, optional): 두 번째 숫자. 기본값은 0입니다.
            
        Returns:
            int: 두 수의 합.
        """
        self.result = self.a + self.b

    def subtract(self):
        """
        두 수의 차를 반환합니다.
        Args:
            self.a (int, optional): 첫 번째 숫자. 기본값은 0입니다.
            self.b (int, optional): 두 번째 숫자. 기본값은 0입니다.
            
        Returns:
            int: 두 수의 차.
        """
        self.result = self.a - self.b

    def multiply(self):
        """
        두 수의 곱을 반환합니다.
        Args:
            self.a (int, optional): 첫 번째 숫자. 기본값은 0입니다.
            self.b (int, optional): 두 번째 숫자. 기본값은 0입니다.
            
        Returns:
            int: 두 수의 곱.
        """
        self.result = self.a * self.b

    def divide(self):
        """
        두 수의 나눗셈 결과를 반환합니다.
        Args:
            self.a (int, optional): 첫 번째 숫자. 기본값은 0입니다.
            self.b (int, optional): 두 번째 숫자. 기본값은 0입니다.
            
        Returns:
            float: 두 수의 나눗셈 결과.
        
        Raises:
            ValueError: 두 번째 숫자가 0인 경우 발생합니다.
        """
        if self.b != 0:
            self.result = self.a / self.b
        else:
            raise ValueError("Division by zero is not allowed.")


class ClassChild(ClassParent):
    """
    ClassChild 클래스는 ClassParent를 상속받아 추가적인 기능을 제공하는 자식 클래스입니다.
    """
    def __init__(self, a=0, b=0):
        super().__init__(a, b)

    def fumnAdd(self):
        self.add()
        return self.result

    def fumnSubtract(self):
        self.subtract()
        return self.result

    def fumnMultiply(self):
        self.multiply()
        return self.result

    def fumnDivide(self):
        self.divide()
        return self.result