import os

os.system("clear")
strName=["a",2,"지예"]

for item in strName:
    print(item)
    

os.system("clear")
print("="*30)

# 리스트는 현재 지정해놓은 크기만큼만 요소를 가질 수 있습니다.
# 이 이상의 데이터는 .append() 메서드를 사용하여 추가할 수 있습니다.
strName.append("우유")

cnt = len(strName)
print(strName)
strName.remove("우유") # 리스트의 특정 영역 삭제
print(strName)

strName.insert(1, "바나나") # 리스트의 특정 위치에 요소 삽입
print(strName)

os.system("clear")
print("="*30)

strTitle=["이름", "국어", "영어", "수학"]
classTitle=[]

titlecnt = len(strTitle)
# for student in range(3):
#     studentInfo=[]
#     for idx in range(titlecnt):
#         studentInfo.append(input(f"{strTitle[idx]} 입력: "))
#     classTitle.append(studentInfo)  
    
# for studentInfo in range(3):
#     for idx in range(titlecnt):
#         print(f"{strTitle[idx]} : {classTitle[studentInfo][idx]}")
        
os.system("clear")
print("="*30)

for student in range(2):
    studentInfo=[]
    for idx in range(titlecnt):
        studentInfo.append(input(f"{strTitle[idx]} 입력: "))
    classTitle.append(studentInfo)  
    
    
print("\n","="*50)
for idx in range(titlecnt):
    print("\t%s" % strTitle[idx], end="")
print("\n","="*50)
for studentInfo in range(2):
    for idx in range(titlecnt):
        print("\t%s" % classTitle[studentInfo][idx], end="")
    print("\n","-"*50)
print("\n","="*50)