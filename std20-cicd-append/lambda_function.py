import json,pymysql,db_conn

# 데이터베이스 연결 재사용을 위한 전역 변수 사용
# db_connection을 재사용하기 위해 self.conn.close()를 호출하지 않고, 연결을 유지하도록 설정
db_connection = db_conn.DBConnection(
    host='proxy-1790901114787-std20-cicd-database.proxy-c5geq8qq2qhl.eu-north-1.rds.amazonaws.com',
    user='std20',
    password='Vwjf[N?s~YsveTs52eQ?h*Zq|a)?',
    db='std20db',
    port=3306
)

def lambda_handler(event, context):
    # 데이터베이스 연결
    cors_headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    db_connection.connect()
    # username = event["queryStringParameters"]["username"] # url 접근시 이렇게 하는 방법도 있지만 이렇게 하지 맙시다.
    # email = event["email"]
    # age = event["age"]
    # ?username=이름&email=메일&age=나이(int)
    query_params = event["queryStringParameters"] or {}
    
    username = query_params["username"]
    email = query_params["email"]
    age = query_params["age"]
    
    #테이블에 행 추가
    try:
        with db_connection.conn.cursor() as cursor:
            
            sql_count = "SELECT count(id) FROM users WHERE email = %s"
            cursor.execute(sql_count, (email,))
            count = cursor.fetchone()
            if count['count(id)'] == 0:
                sql = "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)"
                cursor.execute(sql, (username, email, age))
                print("쿼리 실행 완료")
                cursor.connection.commit()
                return{
                    'statusCode': 200,
                    'headers': {
                        **cors_headers,
                    },
                    'body': json.dumps({
                        'message': 'Row added successfully',
                        'email': email
                    },  ensure_ascii=False)
                }
            else:
                print("Existing rows with the same email:", count)
                return{
                    'statusCode': 409,
                    'headers': cors_headers,
                    'body': json.dumps({'message': 'Email already exists'},  ensure_ascii=False)
                }
    except Exception as e:
        print("에러 :", e)
        db_connection.conn.rollback()
        return{
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'message': 'Internal server error'},  ensure_ascii=False)
        }
    finally:
        if db_connection.conn:
            print("데이터베이스 연결 종료")
            db_connection.conn.close()
            
           
           
            
            
        # return {
        #     'statusCode': 200,
        #     'body': json.dumps('Row added successfully')
        # }