import pymysql

print(pymysql.version_info) # (1, 3, 12, 'final', 0)

config = {
     'host' : '127.0.0.1',
     'user' : 'root',
     'password' : '1234',
     'database' : 'work',
     'port' : 3306,
     'charset':'utf8',
     'use_unicode' : True}

try :
     # db 환경변수 -> db 연동 객체
     conn = pymysql.connect(**config)

        # **config : config에 들어있는 7개의 환경변수를 이용해서 DB를 연동한다는 의미
     # sql 실행 객체
     cursor = conn.cursor()
     print("db 연동 성공!")

     sql = "show tables"
     cursor.execute(sql)
     tables = cursor.fetchall()

     if tables :
          print('table 있음')
     else :
          print('table 없음')

except Exception as e :
     print('db 연동 error :', e)
finally :
     cursor.close()
     conn.close()