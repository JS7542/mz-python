# while 반복문
"""
while 조건:
    실행할 코드
"""
import os
menu = """
[Menu]
    1. 자장면
    2. 짬뽕
    3. 탕수육
    4. 종료
"""
cho = 0
tot = 0
while cho != 4:
    os.system("clear")  # 화면을 지우고 메뉴를 다시 출력
    print(menu)
    cho = int(input("메뉴를 선택하세요: "))
    
    
    print(f"메뉴 선택 횟수: {tot}")
    if tot >= 3 : 
        continue
    tot += 1
    
    # if tot>=3:
    #     print("메뉴 선택 횟수가 3회를 넘었습니다.")
    #     break
    # if cho == 1:
    #     print("자장면을 선택하셨습니다.")
    # elif cho == 2:
    #     print("짬뽕을 선택하셨습니다.")
    # elif cho == 3:
    #     print("탕수육을 선택하셨습니다.")
    # elif cho == 4:
    #     print("프로그램을 종료합니다.")
    # else:
    #     print("잘못된 선택입니다.")
    # input("계속하려면 Enter 키를 누르세요.")