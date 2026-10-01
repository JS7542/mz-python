# 예외 처리
"""
대표 형식

try:
    # 예외가 발생할 수 있는 코드 작성
except [예외 이름[as 변수]]:
    # 예외가 발생했을 때 실행할 코드 작성
else [예외 이름[as 변수]]: 
    # 예외가 발생하지 않았을 때 실행할 코드 작성
        잘 사용하지 않는다.
finally [예외 이름[as 변수]]:
    # 예외 발생 여부와 상관없이 항상 실행할 코드 작성
===================================================
주요 예외이름
ZeroDivisionError: 0으로 나눌 때 발생
ValueError: 잘못된 값이 들어왔을 때 발생
TypeError: 잘못된 자료형이 들어왔을 때 발생
IndexError: 인덱스 범위를 벗어났을 때 발생
KeyError: 딕셔너리에 없는 키를 참조할 때 발생
FileNotFoundError: 파일이 존재하지 않을 때 발생
--- 이후로는 알아놓으면 좋은 예외들
ImportError: 모듈을 불러올 수 없을 때 발생
AttributeError: 객체에 해당 속성이 없을 때 발생
MemoryError: 메모리가 부족할 때 발생
OverflowError: 연산 결과가 너무 커서 표현할 수 없을 때 발생
RuntimeError: 기타 실행 중에 발생하는 오류
StopIteration: 반복자가 더 이상 값을 반환하지 않을 때 발생
KeyboardInterrupt: 사용자가 인터럽트(보통 Ctrl+C)를 발생시켰을 때 발생
"""


def funTest():
    inputdata = input("숫자를 입력하세요: ")
    try:
        num = int(inputdata)
    except ZeroDivisionError as e:
        print("0으로 나눌 수 없습니다. ZeroDivisionError: ", e)
    except IndexError as e: # 리스트
        print("인덱스 범위를 벗어났습니다. IndexError: ", e)
    except KeyError as e:   #딕셔너리
        print("딕셔너리에 없는 키를 참조했습니다. KeyError: ", e)
    except TypeError as e:
        print("잘못된 값이 입력되었습니다. TypeError: ", e)
    except ValueError as e:
        print("잘못된 값이 입력되었습니다. ValueError: ", e)
    except Exception as e:
        print("잘못된 값이 입력되었습니다. Exception: ", e)
    else:
        print(f"입력한 숫자는 {num}입니다.")
    finally:
        print("프로그램 종료")
        

funTest()