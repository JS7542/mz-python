import json, pymysql


class DBConnection:
    def __init__(self, host, user, password, db, port=3306):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'db': db,
            'port': port,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
            'autocommit': False,
            'connect_timeout': 10
        }        
        self.conn = None
    
    def connect(self):
        try:
            # 딕셔너리 언패킹(**Dict): **self.config를 사용하여 pymysql.connect에 전달
            # 딕셔너리 언패킹을 하게되면 딕셔너리의 키이름이 메서드의 파라메타가 되고, 
            # 딕셔너리의 값이 메서드의 파라메타 값이 된다.
            if self.conn is None: # 연결이 없을 경우에만 연결 생성
                self.conn = pymysql.connect(**self.config)
            else:
                self.conn.ping(reconnect=True)  # 연결이 끊어졌을 경우 재연결
            
            with self.conn.cursor() as cursor:
                sql = "SELECT 1"  # 실제 테이블 이름으로 변경
                cursor.execute(sql)
                result = cursor.fetchone()
                print("Query Result:", result)
                
                return self.conn

        except Exception as e:
            print("Error connecting to the database:", e)
            self.conn.rollback()  # 롤백 처리
            return None
            
