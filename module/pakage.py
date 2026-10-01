# 폴더 내부 접근 /  패키지 호출
# 1. 일반적인 모듈 호출

import test.module_sample as module_sample
calc = module_sample.ClassChild(10, 20)
# 2. 별칭 사용

import test.module_sample as ms
calc2 = ms.ClassChild(30, 40)
# 3. 클래스 사용 예제
from test import module_sample
calc3 = module_sample.ClassChild(50, 60)

# 4. 클래스 정의
# from <package>.<module> import <class>
# calc = <class>(<args>)