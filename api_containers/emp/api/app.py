from flask import Flask, jsonify, request
from flask_restful import Api, Resource

#from pymongo import MongoClient

import logging
logging.basicConfig(level=logging.DEBUG)
import bcrypt
import socket

#from bson.json_util import dumps

import json
import pymysql

app = Flask(__name__)
api = Api(app)
logger = logging.getLogger(__name__)


# logging.debug("1")
# mysql_con = pymysql.connect(host='mariadb', port=3306, db='test11', user='root', password='infogen')
#
# logging.debug("2")
# cursor = mysql_con.cursor()
#
# logging.debug("3")
# sql = "SELECT * FROM testpark where a=%s and b=%s"
# cursor.execute(sql ,(a,b,c,))
#
# logging.debug("4")
# result =  cursor.fetchall()
# logging.debug(result)
# mysql_con.close()
#
# print(result)


""" 
HELPER FUNCTIONS
"""

def existsEmail(email):
    # logging.debug(foxTestDb.find({"email": email}).count())
    # if foxTestDb.find({"email": email}).count() == 0:
    #     return False
    # else:

        return True

def getSystemInfo():
    logging.debug('emp Server')
    logging.debug(socket.gethostbyname(socket.gethostname()))
    try:
        if (socket.gethostbyname(socket.gethostname()) == "172.20.0.4" ) :
            logging.debug('Prod Server')
            return "mariadb"
        else :
            logging.debug('Local Server')
            return "218.151.225.142"

    except Exception as e:
        logging.exception(e)
"""
RESOURCES
"""


class Hello(Resource):
    def get(self):
        logging.debug("test")
        return "This is Employee Management API! hohoho"

class Save(Resource):
    def post(self):
        # Get posted data from request
        logging.debug("save start")
        # logging.debug(request)
        # logging.debug(request.get_json())
        # logging.debug(request.get_data())
        # logging.debug(request.form['email'])

        #data = request.get_json()
        # get data
        #id = request.form['id']
        email = request.form['email']
        password = request.form['password']
        addr = request.form['addr']
        sex = request.form['sex']

        logging.debug('--------------------------------------')
        #logging.debug('id : ' + id)
        logging.debug('email : ' + email)
        logging.debug('password : ' + password)
        logging.debug('addr : ' + addr)
        logging.debug('sex : ' + sex)
        logging.debug('--------------------------------------')

        # logging.debug(existsEmail(email))
        if existsEmail(email):
            logging.debug("!!! WARNING !!! email Exists!!")
            retJson = {
                "status": 301,
                "msg": "Already Exists EMAIL"
            }
        else:

            retJson = {
                "status": 200,
                "msg": "Data has been saved successfully"
            }


        return jsonify(retJson)

class Update(Resource):
    def post(self):
        # Get posted data from request
        logging.debug("update start")
        # logging.debug(request)
        logging.debug(request.get_json())
        # logging.debug(request.get_data())
        # logging.debug(request.form['email'])

        upData = request.get_json()
        # get data

        logging.debug(len(upData['data']))

        if len(upData['data']) == 0:
            retJson = {
                "status": 500,
                "msg": "Update Data Not Found"
            }
            return jsonify(retJson)

        for data in upData['data']:

            email = data['email']
            password = data['password']
            addr = data['addr']
            sex = data['sex']

            logging.debug(data)
            logging.debug('--------------------------------------')
            logging.debug('email : ' + email)
            logging.debug('password : ' + password)
            logging.debug('addr : ' + addr)
            logging.debug('sex : ' + sex)
            logging.debug('flag : ' + data['flag'])
            logging.debug('--------------------------------------')

            # if data['flag'] == "U":
            #     #
            #     .update({
            #     #     "email": email
            #     # },
            #     # {'$set':    {
            #     #             "password":password,
            #     #             "addr":addr,
            #     #             "sex":sex
            #     #             }
            #     # })
            # elif data['flag'] == "D":
                # foxTestDb.remove({
                #     "email": email
                # })

        retJson = {
            "status": 200,
            "msg": "Data has been update successfully"
        }

        return jsonify(retJson)

class Search(Resource):
    def get(self):
        # Get posted data from request
        logging.debug("search start")

        # get data
        email = request.args.get('email')

        logging.debug('---------------SEARCH---------------')
        logging.debug('email : ' + email)
        logging.debug('------------------------------------')

        # if email is None or email == "":
        #     logging.debug("is None")
        #     # result = foxTestDb.find()
        # else:
        #     logging.debug("is not null")
        #     # result = foxTestDb.find({
        #     #     "email": email
        #     # })

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='test11', user='root', password='infogen')
        cursor = mysql_con.cursor()

        logging.debug("3")
        if email is None or email == "":
            sql = "SELECT EMP_ID AS EMAIL FROM TB_EMP where EMP_ID=%s and b=%s"
            cursor.execute(sql, (email))
        else:
            logging.debug("is not null")
            sql = "SELECT EMP_ID AS EMAIL FROM TB_EMP "
            cursor.execute(sql)

        result = cursor.fetchall()
        logging.debug(result)
        mysql_con.close()
        logging.debug('---------------RESULT---------------')
        logging.debug(result)
        logging.debug('------------------------------------')
        array = list(result)  # 결과를 리스트로
        logging.debug(array)
        logging.debug(dumps(array))  # 리스트파일은 dumps
        logging.debug(jsonify(dumps(array)))  # dumps한 파일은 jsonify

        retJson = {
            "status": 200,
            "msg": "Data has been saved successfully"
        }

        return jsonify(dumps(array))

class Health(Resource):
    def get(self):
        retJson = {
            "status": "UP"
        }
        return jsonify(retJson)

class Id(Resource):
    def get(self):
        logging.debug("idChektest start")

        logging.debug(request)
        id = request.args.get('id')
        # logging.debug(foxTestDb.find({"id": id}).count())

        # if foxTestDb.find({"id": id}).count() == 0:
        #     result = {"result" : "False"}
        # else:
        #     result = {"result" : "True"}
        result = "";
        logging.debug(result)

        return result

class SignUp(Resource):
    def post(self):
        # Get posted data from request
        logging.debug("save start")

        #data = request.get_json()
        # get data
        id = request.form['id']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        logging.debug('--------------------------------------')
        logging.debug('id : ' + id)
        logging.debug('email : ' + email)
        logging.debug('password : ' + password)
        logging.debug('phone : ' + phone)
        logging.debug('--------------------------------------')

        # logging.debug(existsEmail(email))
        if existsEmail(email):
            logging.debug("!!! WARNING !!! email Exists!!")
            retJson = {
                "status": 301,
                "msg": "Already Exists EMAIL"
            }
        else:
            # foxTestDb.insert({
            #     "id" : id,
            #     "email": email,
            #     "password": password,
            #     "phone" : phone
            # })
            retJson = {
                "status": 200,
                "msg": "Data has been saved successfully"
            }

        return jsonify(retJson)


class Search2(Resource):
    def get(self):
        # Get posted data from request
        logging.debug("search start")

        # get data
        id = request.args.get('id')
        email = request.args.get('email')
        passwd = request.args.get('password')

        logging.debug('---------------SEARCH---------------')
        logging.debug('email : ' + email)
        logging.debug('id : ' + id)
        logging.debug('passwd : ' + passwd)
        logging.debug('------------------------------------')

        logging.debug("is not null id")

        mysql_con = pymysql.connect(getSystemInfo(), port='3306:3306', db='test11', user='root', password='infogen',charset ='utf8')

        try :
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                if email is None or email == "":
                    logging.debug("search2 all data")
                    sql = "SELECT * FROM TB_EMP "
                    cursor.execute(sql)
                else:
                    logging.debug("is not null")
                    sql = "SELECT EMP_ID AS EMAIL FROM TB_EMP where EMP_ID=%s "
                    cursor.execute(sql, (email))

        finally:
            mysql_con.close()

        result = cursor.fetchall()
        for row in result :
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        logging.debug('---------------RESULT---------------')
        logging.debug(result)
        logging.debug('------------------------------------')
        array = list(result)  # 결과를 리스트로
        logging.debug(array)
        logging.debug(dumps(array))  # 리스트파일은 dumps
        logging.debug(jsonify(dumps(array)))  # dumps한 파일은 jsonify

        # retJson = {
        #     "status": 200,
        #     "msg": "Data has been saved successfully"
        # }
        return jsonify(dumps(array))
class empReferenceInit(Resource):
    def get(self):
        # Get posted data from request
        logging.debug("empReferenceInit")

        # get data
        id = request.args.get('id')
        email = request.args.get('email')
        passwd = request.args.get('password')

        logging.debug('---------------SEARCH---------------')
        logging.debug('id : ' + id)
        logging.debug('------------------------------------')


        mysql_con = pymysql.connect(getSystemInfo(), port='3306', db='test11', user='root', password='infogen',charset ='utf8')
        logging.debug('init sql end')
        try :
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM EMP_API_TB_EMP "
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result = cursor.fetchall()
        for row in result :
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        logging.debug('---------------RESULT---------------')
        logging.debug(result)
        logging.debug('------------------------------------')
        array = list(result)  # 결과를 리스트로
        logging.debug(array)
        logging.debug(dumps(array))  # 리스트파일은 dumps
        logging.debug(jsonify(dumps(array)))  # dumps한 파일은 jsonify

        # retJson = {
        #     "status": 200,
        #     "msg": "Data has been saved successfully"
        # }
        #return jsonify(dumps(array))
        return result

class testDB(Resource):
    def get(self):
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM WEB_CONN_TEST "
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return result2

class mariatestDB(Resource): # Mariadb 연결 진행
    def get(self):
        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8')
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT * FROM WEB_CONN_TEST "
                cursor.execute(sql)

                mysql_con.commit();

        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return result2

class SingIn(Resource): # 사용자 정보 조회
    def post(self):
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8')

        params = request.get_json()

        logging.debug("EMP Login Start")
        emp_id = request.form['emp_id']
        emp_pw = request.form['emp_pw']
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT * FROM TB_EMP_MGMT WHERE BINARY EMP_ID =%s AND EMP_PW =%s"
                cursor.execute(sql,(emp_id,emp_pw))

                mysql_con.commit();

        finally:
            mysql_con.close()

        result2 = cursor.fetchone()
        if result2 is not None :
            retJson = {
                "status": 200,
                "msg": "Data has been saved successfully",
                "email": result2['EMP_EMAIL']
            }
        else :
            retJson = {
                "status": 400,
                "msg": "No Data"
            }
        # for row in result2:
        #     logging.debug('====== row====')
        #     logging.debug(row)
        #     logging.debug('===============')
        # array = list(result2)  # 결과를 리스트로
        logging.debug(retJson)


        return jsonify(retJson)

class authSearch(Resource):  # 사용자 권한 조회
    def post(self):
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8')
        params = request.get_json()

        logging.debug("EMP Auth Start")
        emp_id = request.form['emp_id']
        logging.debug("EMP Auth Start")
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT AUTH_ID FROM TB_EMP_MGMT WHERE EMP_ID =%s"
                cursor.execute(sql, (emp_id))

        finally:
            mysql_con.close()

        result2 = cursor.fetchone()
        logging.debug(result2)
        if result2 is not None:
            retJson = {
                "status": 200,
                "msg": "Data has been saved successfully",
                "auth" : result2['AUTH_ID']
            }
        else:
            retJson = {
                "status": 400,
                "msg": "No Data"
            }
            # for row in result2:
            #     logging.debug('====== row====')
            #     logging.debug(row)
            #     logging.debug('===============')
            # array = list(result2)  # 결과를 리스트로
        logging.debug(retJson)

        return jsonify(retJson)
#
api.add_resource(Hello, '/hello')
api.add_resource(Save, '/save')
api.add_resource(Update, '/update')
api.add_resource(Search, '/search')
api.add_resource(Health, '/health')
#신규 추가
api.add_resource(Id,'/idChektest')
api.add_resource(SignUp,'/signUp')
api.add_resource(Search2,'/search2')
api.add_resource(empReferenceInit,'/empReferenceInit')
api.add_resource(testDB,'/testDB')
api.add_resource(mariatestDB,'/mariatestDB') #api 선언
api.add_resource(SingIn,'/SingIn')
api.add_resource(authSearch,'/authSearch')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)