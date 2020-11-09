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

import datetime
from json import JSONEncoder

class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

def getSystemInfo():
    logging.debug('dill Server')
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


def dateConverter(param):
    if isinstance(param, datetime.datetime):
        return param.__str__()


def userExist(username):
    if users.find({"Username": username}).count() == 0:
        return False
    else:
        return True


def verifyUser(username, password):
    if not userExist(username):
        return False

    user_hashed_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.checkpw(password.encode('utf8'), user_hashed_pw):
        return True
    else:
        return False


def getUserMessages(username):
    # get the messages
    return users.find({
        "Username": username,
    })[0]["Messages"]


"""
RESOURCES
"""


class Hello(Resource):
    def get(self):
        return "This is Dili Management API!"


class Register(Resource):
    def post(self):
        # Get posted data from request
        data = request.get_json()

        # get data
        username = data["username"]
        password = data["password"]

        # check if user exists
        if userExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonify(retJson)

        # encrypt password
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # Insert record
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Messages": []
        })

        # Return successful result
        retJosn = {
            "status": 200,
            "msg": "Registration successful"
        }
        return jsonify(retJosn)


class Retrieve(Resource):
    def post(self):
         # Get posted data from request
        data = request.get_json()

        # get data
        username = data["username"]
        password = data["password"]

        # check if user exists
        if not userExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonify(retJson)

        # check password
        correct_pw = verifyUser(username, password)
        if not correct_pw:
            retJson = {
                "status": 302,
                "msg": "Invalid password"
            }
            return jsonify(retJson)

        # get the messages
        messages = getUserMessages(username)

        # Build successful response
        retJson = {
            "status": 200,
            "obj": messages
        }

        return jsonify(retJson)


class Save(Resource):
    def post(self):

         # Get posted data from request
        data = request.get_json()

        # get data
        username = data["username"]
        password = data["password"]
        message = data["message"]

        # check if user exists
        if not userExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonify(retJson)

        # check password
        correct_pw = verifyUser(username, password)
        if not correct_pw:
            retJson = {
                "status": 302,
                "msg": "Invalid password"
            }
            return jsonify(retJson)

        if not message:
            retJson = {
                "status": 303,
                "msg": "Please supply a valid message"
            }
            return jsonify(retJson)

        # get the messages
        messages = getUserMessages(username)

        # add new message
        messages.append(message)

        # save the new user message
        users.update({
            "Username": username
        }, {
            "$set": {
                "Messages": messages
            }
        })

        retJson = {
            "status": 200,
            "msg": "Message has been saved successfully"
        }

        return jsonify(retJson)


class mariatestDB(Resource): # Mariadb 연결 진행
    def get(self):

        logging.debug(request.get_json())

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo() , port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
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

class yryMgmt(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT * FROM TB_YRY_MGMT_M WHERE EMP_EMAL_ADDR = '" + data["email"] + "'"
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


class weekGridData(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        logging.debug('================== App Start ==================')
        logging.debug(data)
        logging.debug('================== App End ==================')

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT  A.EMP_EMAL_ADDR "\
                    + "       ,A.WRK_DT "\
                    + "       ,NVL(DATE_FORMAT(A.JOB_STRT_TM, '%H:%i:%s'),'-') AS JOB_STRT_TM "\
                    + "       ,NVL(DATE_FORMAT(A.JOB_END_TM, '%H:%i:%s'),'-') AS JOB_END_TM "\
                    + "       ,CONCAT(SUBSTRING(A.NORM_WRK_TM,1,2),':',SUBSTRING(A.NORM_WRK_TM,3,2),':',SUBSTRING(A.NORM_WRK_TM,5,2)) AS NORM_WRK_TM "\
                    + "       ,CONCAT(SUBSTRING(A.ALL_WRK_TM,1,2),':',SUBSTRING(A.ALL_WRK_TM,3,2),':',SUBSTRING(A.ALL_WRK_TM,5,2)) AS ALL_WRK_TM "\
                    + "       ,DATE_FORMAT(SEC_TO_TIME(TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.ALL_WRK_TM,1,2),':',SUBSTRING(A.ALL_WRK_TM,3,2),':',SUBSTRING(A.ALL_WRK_TM,5,2)) ,'%H:%i:%S')) "\
                    + "                   - TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.NORM_WRK_TM,1,2),':',SUBSTRING(A.NORM_WRK_TM,3,2),':',SUBSTRING(A.NORM_WRK_TM,5,2)) ,'%H:%i:%S'))),'%H:%i:%s') AS OVER_WRK_TM " \
                    + "       ,NVL(B.APVL_REQ_DIVS, 'N/A') AS APVL_REQ_DIVS " \
                    + "       ,NVL(B.APVL_REQ_DT, 'N/A') AS APVL_REQ_DT "\
                    + "       ,NVL(B.APVL_LAST_APRV_DT, 'N/A') AS APVL_LAST_APRV_DT "\
                    + "   FROM TB_WRK_TM_MGMT_M A "\
                    + "        LEFT OUTER JOIN TB_APVL_REQ_MGMT_M B"\
                    + "   ON A.WRK_DT = B.WRK_DT "\
                    + "   AND A.EMP_EMAL_ADDR = B.EMP_EMAL_ADDR "\
                    + "  WHERE 1 = 1 "\
                    + "  AND A.EMP_EMAL_ADDR = '" + data["email"] + "' "\
                    + "  AND A.WRK_DT >= '" + data["strtDt"] + "' "\
                    + "  AND A.WRK_DT <= '" + data["endDt"] + "' "\
                    + "  ORDER BY A.WRK_DT"
                logging.debug(sql)
                cursor.execute(sql)
        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row2====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)

class apvlInfo(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        logging.debug('================== App Start ==================')
        logging.debug(data)
        logging.debug('================== App End ==================')

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT  NVL(APVL_REQ_DT, 'N/A') AS APVL_REQ_DT "\
                    + "       ,NVL(APVL_LAST_APRV_DT, 'N/A') AS APVL_LAST_APRV_DT "\
                    + "     FROM TB_APVL_REQ_MGMT_M "\
                    + "   WHERE EMP_EMAL_ADDR = '" + data["email"] + "' "\
                    + "   AND WRK_DT = '" + data["dt"] + "'"
                logging.debug(sql)
                cursor.execute(sql)
        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row2====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)

class monthGridData(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        logging.debug('================== App Start ==================')
        logging.debug(data)
        logging.debug('================== App End ==================')

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT  A.EMP_EMAL_ADDR "\
                    + "       ,A.WRK_DT "\
                    + "       ,NVL(DATE_FORMAT(A.JOB_STRT_TM, '%H:%i:%s'),'-') AS JOB_STRT_TM "\
                    + "       ,NVL(DATE_FORMAT(A.JOB_END_TM, '%H:%i:%s'),'-') AS JOB_END_TM "\
                    + "       ,CONCAT(SUBSTRING(A.NORM_WRK_TM,1,2),':',SUBSTRING(A.NORM_WRK_TM,3,2),':',SUBSTRING(A.NORM_WRK_TM,5,2)) AS NORM_WRK_TM "\
                    + "       ,CONCAT(SUBSTRING(A.ALL_WRK_TM,1,2),':',SUBSTRING(A.ALL_WRK_TM,3,2),':',SUBSTRING(A.ALL_WRK_TM,5,2)) AS ALL_WRK_TM "\
                    + "       ,DATE_FORMAT(SEC_TO_TIME(TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.ALL_WRK_TM,1,2),':',SUBSTRING(A.ALL_WRK_TM,3,2),':',SUBSTRING(A.ALL_WRK_TM,5,2)) ,'%H:%i:%S')) "\
                    + "                   - TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.NORM_WRK_TM,1,2),':',SUBSTRING(A.NORM_WRK_TM,3,2),':',SUBSTRING(A.NORM_WRK_TM,5,2)) ,'%H:%i:%S'))),'%H:%i:%s') AS OVER_WRK_TM "\
                    + "       ,NVL(B.APVL_REQ_DIVS, 'N/A') AS APVL_REQ_DIVS "\
                    + "       ,NVL(B.APVL_REQ_DT, 'N/A') AS APVL_REQ_DT "\
                    + "       ,NVL(B.APVL_LAST_APRV_DT, 'N/A') AS APVL_LAST_APRV_DT "\
                    + "   FROM TB_WRK_TM_MGMT_M A "\
                    + "        LEFT OUTER JOIN TB_APVL_REQ_MGMT_M B"\
                    + "   ON A.WRK_DT = B.WRK_DT "\
                    + "   AND A.EMP_EMAL_ADDR = B.EMP_EMAL_ADDR "\
                    + "  WHERE 1 = 1 "\
                    + "  AND A.EMP_EMAL_ADDR = '" + data["email"] + "' "\
                    + "  AND A.WRK_DT like '"+data["mDt"]+"%' "\
                    + "  ORDER BY A.WRK_DT"
                logging.debug(sql)
                cursor.execute(sql)
        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row2====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)

class wrkTimeInfoByEml(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        logging.debug('================== App Startasd ==================')
        logging.debug(data)
        logging.debug('================== App End ==================')

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT A.EMP_EMAL_ADDR" \
                    + "      ,A.WRK_DT" \
                    + "      ,DATE_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.NORM_WRK_TM,1,2),':',SUBSTRING(A.NORM_WRK_TM,3,2),':',SUBSTRING(A.NORM_WRK_TM,5,2)) ,'%H:%i:%S')))),'%H.%i') NORM_WRK_TM" \
                    + "      ,DATE_FORMAT(SEC_TO_TIME((SUM(TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.HLDY_WRK_TM,1,2),':',SUBSTRING(A.HLDY_WRK_TM,3,2),':',SUBSTRING(A.HLDY_WRK_TM,5,2)) ,'%H:%i:%S'))) + SUM(TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.NGHT_WRK_TM,1,2),':',SUBSTRING(A.NGHT_WRK_TM,3,2),':',SUBSTRING(A.NGHT_WRK_TM,5,2)) ,'%H:%i:%S')))) - SUM(TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(IFNULL(B.WRK_TME,'000000'),1,2),':',SUBSTRING(IFNULL(B.WRK_TME,'000000'),3,2),':',SUBSTRING(IFNULL(B.WRK_TME,'000000'),5,2)) ,'%H:%i:%S')))),'%H.%i') NOT_APRV_OVER_WRK_TM" \
                    + "      ,DATE_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(IFNULL(B.WRK_TME,'000000'),1,2),':',SUBSTRING(IFNULL(B.WRK_TME,'000000'),3,2),':',SUBSTRING(IFNULL(B.WRK_TME,'000000'),5,2)) ,'%H:%i:%S')))),'%H.%i') APRV_OVER_WRK_TM" \
                    + "  FROM TB_WRK_TM_MGMT_M A LEFT OUTER JOIN TB_APVL_REQ_MGMT_M B ON A.EMP_EMAL_ADDR = B.EMP_EMAL_ADDR AND A.WRK_DT = B.WRK_DT AND B.APVL_REQ_DIVS IN ('01','02')" \
                    + " WHERE A.EMP_EMAL_ADDR = '" +data["email"] + "'" \
                    + "   AND DATE(A.WRK_DT) BETWEEN DATE('" + data["strtDate"] + "') AND DATE('" + data["endDate"] + "')" \
                    + " GROUP BY A.EMP_EMAL_ADDR"
                logging.debug(sql)
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)

class wrkApvlReq(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT A.WRK_DT" \
                      "     , CASE WHEN NVL(A.HLDY_WRK_TM,'') != 000000" \
                      "            THEN A.HLDY_WRK_TM" \
                      "            WHEN NVL(A.NGHT_WRK_TM,'') != 000000" \
                      "            THEN A.NGHT_WRK_TM" \
                      "            ELSE '' END WRK_TME" \
                      "     , CASE WHEN NVL(A.HLDY_WRK_TM,'') != 000000 AND NVL(A.NGHT_WRK_TM,'') = 000000 THEN '휴일근무' " \
                      "            WHEN NVL(A.HLDY_WRK_TM,'') = 000000 AND NVL(A.NGHT_WRK_TM,'') != 000000 THEN '야근근무' " \
                      "            ELSE '' END WRK_TYPE " \
                      "  FROM TB_WRK_TM_MGMT_M A" \
                      " WHERE A.EMP_EMAL_ADDR = '" + data["email"] + "'" \
                      "   AND (NVL(A.HLDY_WRK_TM,'000000') != 000000 OR NVL(A.NGHT_WRK_TM,'000000') != 000000)" \
                      "   AND NOT EXISTS (SELECT 1" \
                      "                     FROM TB_APVL_REQ_MGMT_M B" \
                      "                    WHERE B.EMP_EMAL_ADDR = A.EMP_EMAL_ADDR" \
                      "                      AND B.WRK_DT = A.WRK_DT)"
                logging.debug("wrkApvlReq SQL문" + sql)
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)
    
class saveApvlReq(Resource): # Mariadb 연결 진행
    def post(self):

        params = request.get_json()
        logger.info(params)

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        email = request.form['email']
        apvlReqDivs = request.form['apvlReqDivs']
        wrkDt = request.form['wrkDt'] 
        wrkTme = request.form['wrkTme']
        wrkReqRsn = request.form['wrkReqRsn']
        th1AprvStus = request.form['th1AprvStus']
        th1AprvNm = request.form['th1AprvNm']
        th2AprvStus = request.form['th2AprvStus']
        th2AprvNm = request.form['th2AprvNm']
        
            

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "INSERT INTO TB_APVL_REQ_MGMT_M (" \
                                                      "`EMP_EMAL_ADDR`," \
                                                      "`APVL_REQ_DIVS`," \
                                                      "`WRK_DT`," \
                                                      "`WRK_TME`," \
                                                      "`WRK_REQ_RSN`," \
                                                      "`APVL_REQ_DT`," \
                                                      "`TH1_APRV_STUS`," \
                                                      "`TH1_APRV_NM`," \
                                                      "`TH2_APRV_STUS`," \
                                                      "`TH2_APRV_NM`," \
                                                      "`APVL_LAST_APRV_DT`)" \
                                                      "VALUES( %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, NOW())" \
                
                # "ON DUPLICATE KEY UPDATE "
                # "EMP_EMAL_ADDR = %s, " \
                # "APVL_REQ_DIVS = %s," \
                # "WRK_DT = %s," \
                # "WRK_TME = %s," \
                # "WRK_REQ_RSN = %s," \
                # "TH1_APRV_STUS = %s," \
                # "TH1_APRV_NM = %s," \
                # "TH2_APRV_STUS = %s," \
                # "TH2_APRV_NM = %s,"
                logger.info(sql)
                cursor.execute(sql, (email, apvlReqDivs, wrkDt, wrkTme, wrkReqRsn, th1AprvStus, th1AprvNm, th2AprvStus, th2AprvNm))
                
                mysql_con.commit()

        finally:
            mysql_con.close()

            retJson = {
                "status": 200,
                "msg": "Data has been saved successfully"
            }

        return jsonify(retJson)
    
class apvlReqHist(Resource): # Mariadb 연결 진행
    def get(self):

        # get data
        data = request.get_json()

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                if data["apvlStusDivs"] == "00":
                    #전체
                    sql = "SELECT B.EMP_NAME" \
                          "      ,NVL(A.WRK_DT,'') WRK_DT" \
                          "      ,CASE WHEN A.APVL_REQ_DIVS = '01' THEN NVL(A.WRK_TME,'') " \
                          "            WHEN A.APVL_REQ_DIVS = '02' THEN NVL(A.WRK_TME,'') " \
                          "            ELSE '' END WRK_TME  " \
                          "      ,CASE WHEN A.APVL_REQ_DIVS = '01' THEN '휴일근무' " \
                          "            WHEN A.APVL_REQ_DIVS = '02' THEN '야근근무' " \
                          "            WHEN A.APVL_REQ_DIVS = '03' THEN '연차결재'  " \
                          "            ELSE '' END APVL_REQ_NM  " \
                          "      ,CASE WHEN A.TH1_APRV_STUS != '' AND A.TH2_APRV_STUS = '' THEN '미승인'" \
                          "            WHEN A.TH1_APRV_STUS != '' AND A.TH2_APRV_STUS != '' THEN '승인'" \
                          "            ELSE '미승인' END APRV_STUS_NM" \
                          "  FROM TB_APVL_REQ_MGMT_M A, TB_EMP_MGMT B" \
                          " WHERE A.EMP_EMAL_ADDR = B.EMP_EMAIL" \
                          "   AND A.EMP_EMAL_ADDR = '" + data["email"] + "'"
                    logging.debug("apvlReqHist SQL문" + sql)
                    cursor.execute(sql)
                if data["apvlStusDivs"] == "01":
                    #미승인
                    sql = "SELECT B.EMP_NAME" \
                          "      ,NVL(A.WRK_DT,'') WRK_DT" \
                          "      ,CASE WHEN A.APVL_REQ_DIVS = '01' THEN NVL(A.WRK_TME,'') " \
                          "            WHEN A.APVL_REQ_DIVS = '02' THEN NVL(A.WRK_TME,'') " \
                          "            ELSE '' END WRK_TME  " \
                          "      ,CASE WHEN A.APVL_REQ_DIVS = '01' THEN '휴일근무' " \
                          "            WHEN A.APVL_REQ_DIVS = '02' THEN '야근근무' " \
                          "            WHEN A.APVL_REQ_DIVS = '03' THEN '연차결재'  " \
                          "            ELSE '' END APVL_REQ_NM  " \
                          "      ,CASE WHEN A.TH1_APRV_STUS != '' AND A.TH2_APRV_STUS = '' THEN '미승인'" \
                          "            WHEN A.TH1_APRV_STUS != '' AND A.TH2_APRV_STUS != '' THEN '승인'" \
                          "            ELSE '미승인' END APRV_STUS_NM" \
                          "  FROM TB_APVL_REQ_MGMT_M A, TB_EMP_MGMT B" \
                          " WHERE A.EMP_EMAL_ADDR = B.EMP_EMAIL" \
                          "   AND A.EMP_EMAL_ADDR = '" + data["email"] + "'"\
                          "   AND (NVL(A.TH1_APRV_STUS,'') NOT IN ('01','02') OR NVL(A.TH2_APRV_STUS,'') NOT IN ('01','02'))"
                    logging.debug("apvlReqHist SQL문" + sql)
                    cursor.execute(sql)
                if data["apvlStusDivs"] == "02":
                    #승인
                    sql = "SELECT B.EMP_NAME" \
                          "      ,NVL(A.WRK_DT,'') WRK_DT" \
                          "      ,CASE WHEN A.APVL_REQ_DIVS = '01' THEN NVL(A.WRK_TME,'') " \
                          "            WHEN A.APVL_REQ_DIVS = '02' THEN NVL(A.WRK_TME,'') " \
                          "            ELSE '' END WRK_TME  " \
                          "      ,CASE WHEN A.APVL_REQ_DIVS = '01' THEN '휴일근무' " \
                          "            WHEN A.APVL_REQ_DIVS = '02' THEN '야근근무' " \
                          "            WHEN A.APVL_REQ_DIVS = '03' THEN '연차결재'  " \
                          "            ELSE '' END APVL_REQ_NM  " \
                          "      ,CASE WHEN A.TH1_APRV_STUS != '' AND A.TH2_APRV_STUS = '' THEN '미승인'" \
                          "            WHEN A.TH1_APRV_STUS != '' AND A.TH2_APRV_STUS != '' THEN '승인'" \
                          "            ELSE '미승인' END APRV_STUS_NM" \
                          "  FROM TB_APVL_REQ_MGMT_M A, TB_EMP_MGMT B" \
                          " WHERE A.EMP_EMAL_ADDR = B.EMP_EMAIL" \
                          "   AND A.EMP_EMAL_ADDR = '" + data["email"] + "'"\
                          "   AND A.TH1_APRV_STUS IN ('01', '02')" \
                          "   AND A.TH2_APRV_STUS IN ('01', '02')"
                    logging.debug("apvlReqHist SQL문" + sql)
                    cursor.execute(sql)

        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)


class empList(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()
        # get data
        email = data["email"]

        logging.debug('================== App Start ==================')
        logging.debug(data)
        logging.debug(data["email"])
        logging.debug('================== App End ==================')

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                if email == "List":
                    sql = "SELECT SEQ_NO, EMP_NAME, EMP_EMAIL, EMP_TEL FROM TB_EMP_MGMT ORDER BY SEQ_NO"
                else:
                    sql = "SELECT SEQ_NO, EMP_NAME, EMP_EMAIL, EMP_TEL FROM TB_EMP_MGMT WHERE EMP_EMAIL like '%" + data["email"] + "%' ORDER BY SEQ_NO"

                logging.debug(sql)
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)

class empInfo(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        # get data
        #name = data["name"]

        logging.debug('================== App Start ==================')
        logging.debug(data)
        logging.debug(data["name"])
        logging.debug(request.args.get('name'))
        logging.debug(request.args.get('param'))
        logging.debug('================== App End ==================')

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT SEQ_NO, EMP_NAME, EMP_EMAIL, EMP_TEL FROM TB_EMP_MGMT WHERE EMP_NAME LIKE '%" + data["name"] + "%' ORDER BY SEQ_NO"

                logging.debug(sql)
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)

    
class apvlReqHistDetl(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT NVL(B.EMP_NAME,'') TH1_APRV_NM" \
                    + "      ,NVL(C.EMP_NAME,'') TH2_APRV_NM" \
                    + "      ,CASE WHEN A.TH1_APRV_STUS != '' THEN '승인'" \
                    + "            ELSE '미승인' END TH1_APRV_STUS_NM" \
                    + "      ,CASE WHEN A.TH2_APRV_STUS != '' THEN '승인'" \
                    + "            ELSE '미승인' END TH2_APRV_STUS_NM" \
                    + "   FROM TB_APVL_REQ_MGMT_M A, TB_EMP_MGMT B, TB_EMP_MGMT C " \
                    + "  WHERE A.TH1_APRV_NM = B.EMP_EMAIL" \
                    + "    AND A.TH2_APRV_NM = C.EMP_EMAIL" \
                    +  "   AND A.EMP_EMAL_ADDR = '" + data["email"] + "'"
                logging.debug("apvlReqHist SQL문" + sql)
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)

class calendarData(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        logging.debug('================== App Start ==================')
        logging.debug(data)
        logging.debug(data["email"])
        logging.debug('================== App End ==================')

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT    A.EMP_EMAL_ADDR " \
                      + "       ,A.WRK_DT " \
                      + "       ,NVL(DATE_FORMAT(A.JOB_STRT_TM, '%H:%i:%s'),'-') AS JOB_STRT_TM " \
                      + "       ,NVL(DATE_FORMAT(A.JOB_END_TM, '%H:%i:%s'),'-') AS JOB_END_TM " \
                      + "       ,A.NORM_WRK_TM " \
                      + "       ,A.ALL_WRK_TM " \
                      + "       ,NVL(B.APVL_REQ_DIVS, 'N/A') AS APVL_REQ_DIVS " \
                      + "       ,NVL(B.APVL_REQ_DT, 'N/A') AS APVL_REQ_DT " \
                      + "       ,NVL(B.APVL_LAST_APRV_DT, 'N/A') AS APVL_LAST_APRV_DT " \
                      + "       ,DATE_FORMAT(SEC_TO_TIME(TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.ALL_WRK_TM,1,2),':',SUBSTRING(A.ALL_WRK_TM,3,2),':',SUBSTRING(A.ALL_WRK_TM,5,2)) ,'%H:%i:%S')) " \
                      + "                   - TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.NORM_WRK_TM,1,2),':',SUBSTRING(A.NORM_WRK_TM,3,2),':',SUBSTRING(A.NORM_WRK_TM,5,2)) ,'%H:%i:%S'))),'%H:%i:%s') AS OVER_WRK_TM " \
                      + "   FROM TB_WRK_TM_MGMT_M A " \
                      + "        LEFT OUTER JOIN TB_APVL_REQ_MGMT_M B" \
                      + "     ON A.WRK_DT = B.WRK_DT " \
                      + "    AND A.EMP_EMAL_ADDR = B.EMP_EMAL_ADDR " \
                      + "  WHERE 1 = 1 " \
                      + "    AND A.EMP_EMAL_ADDR = '" + data["email"] + "'"\
                      + "    AND A.WRK_DT LIKE '" + data["dt"] + "%'"

                logging.debug(sql)
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)


class noticeLst(Resource):  # Mariadb 연결 진행
    def get(self):
        logging.debug("noticeLst start")
        logging.debug(request.get_json())

        # get data
        category = request.args.get('category')
        searchStr = request.args.get('searchStr')

        logging.debug('---------------SEARCH---------------')
        logging.debug('category : ' + category)
        logging.debug('searchStr : ' + searchStr)
        logging.debug('------------------------------------')

        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                # sql = "SELECT TIT, CNTN, KD_DIVS_CD, MJR_YN, POP_OPEN_YN, DATA_INPT_ID, DATA_INPT_PGM_ID, DATA_UPD_ID, DATA_UPD_PGM_ID FROM TB_STTS_POST_MGMT_M "
                sql = "SELECT  A.POST_ID, " \
                      "A.TIT, " \
                      "A.CNTN, " \
                      "A.KD_DIVS_CD, " \
                      "A.MJR_YN, " \
                      "A.POP_OPEN_YN, " \
                      "A.DATA_INPT_ID, " \
                      "B.EMP_NAME, " \
                      "DATE_FORMAT(A.DATA_INPT_DTTM, '%Y-%m-%d %H:%i:%s') AS DATA_INPT_DTTM, " \
                      "A.DATA_INPT_PGM_ID, " \
                      "A.DATA_UPD_ID, " \
                      "DATE_FORMAT(A.DATA_UPD_DTTM, '%Y-%m-%d %H:%i:%s') AS DATA_UPD_DTTM, " \
                      "A.DATA_UPD_PGM_ID, " \
                      "CASE WHEN A.KD_DIVS_CD = '01' THEN '공지' " \
                      "WHEN A.KD_DIVS_CD = '02' THEN '복리' " \
                      "WHEN A.KD_DIVS_CD = '03' THEN '발령'  " \
                      "WHEN A.KD_DIVS_CD = '04' THEN '그룹웨어'  " \
                      "ELSE '' END KD_DIVS_NM  " \
                      "FROM  TB_STTS_POST_MGMT_M A LEFT OUTER JOIN TB_EMP_MGMT B ON A.DATA_INPT_ID = B.EMP_EMAIL " \
                      "WHERE 1=1 " \
                      "AND  post_id IN ( " \
                      "		              SELECT AA.POST_ID FROM  " \
                      "		                                    ( " \
                      "		                                    	SELECT ROW_NUMBER() OVER (ORDER BY POST_ID DESC) AS ROW_NUM, POST_ID " \
                      "		                                    	FROM TB_STTS_POST_MGMT_M  " \
                      "		                                    	WHERE MJR_YN = 'Y'  " \
                      "		                                    	ORDER BY POST_ID DESC " \
                      "		                                    ) AA " \
                      "		              WHERE  AA.ROW_NUM <= 3 " \
                      "	) " \
                      "UNION " \
                      "SELECT  A.POST_ID, " \
                      "A.TIT, " \
                      "A.CNTN, " \
                      "A.KD_DIVS_CD, " \
                      "A.MJR_YN, " \
                      "A.POP_OPEN_YN, " \
                      "A.DATA_INPT_ID, " \
                      "B.EMP_NAME, " \
                      "DATE_FORMAT(A.DATA_INPT_DTTM, '%Y-%m-%d %H:%i:%s') AS DATA_INPT_DTTM, " \
                      "A.DATA_INPT_PGM_ID, " \
                      "A.DATA_UPD_ID, " \
                      "DATE_FORMAT(A.DATA_UPD_DTTM, '%Y-%m-%d %H:%i:%s') AS DATA_UPD_DTTM, " \
                      "A.DATA_UPD_PGM_ID, " \
                      "CASE WHEN A.KD_DIVS_CD = '01' THEN '공지' " \
                      "WHEN A.KD_DIVS_CD = '02' THEN '복리' " \
                      "WHEN A.KD_DIVS_CD = '03' THEN '발령'  " \
                      "WHEN A.KD_DIVS_CD = '04' THEN '그룹웨어'  " \
                      "ELSE '' END KD_DIVS_NM  " \
                      "FROM  TB_STTS_POST_MGMT_M A LEFT OUTER JOIN TB_EMP_MGMT B ON A.DATA_INPT_ID = B.EMP_EMAIL " \
                      "WHERE 1=1 "
                if searchStr != "":
                    if category == "00":
                        sql += "AND TIT LIKE '%" + searchStr + "%' "
                    if category == "01":
                        sql += "AND CNTN LIKE '%" + searchStr + "%' "
                    if category == "02":
                        sql += "AND (TIT LIKE '%" + searchStr + "%' OR CNTN LIKE '%" + searchStr + "%') "
                    if category == "03":
                        sql += "AND B.EMP_NAME LIKE '%" + searchStr + "%' "
                sql += "ORDER BY MJR_YN DESC, POST_ID DESC "
                logging.debug(sql)
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        # for row in result2:
        #    logging.debug('====== row====')
        #    logging.debug(row)
        #    logging.debug('===============')
        # array = list(result2)  # 결과를 리스트로

        return result2


class noticeOne(Resource):  # Mariadb 연결 진행
    def get(self):
        logging.debug("noticeOne start")
        logging.debug(request.get_json())

        # get data
        postId = request.args.get('postId')

        logging.debug('---------------SEARCH---------------')
        logging.debug('postId : ' + postId)
        logging.debug('------------------------------------')

        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT  A.POST_ID, " \
                      "A.TIT, " \
                      "A.CNTN, " \
                      "A.KD_DIVS_CD, " \
                      "A.MJR_YN, " \
                      "A.POP_OPEN_YN, " \
                      "A.POP_OPEN_DTTM_FROM, " \
                      "A.POP_OPEN_DTTM_TO, " \
                      "A.DATA_INPT_ID, " \
                      "B.EMP_NAME, " \
                      "A.DATA_INPT_PGM_ID, " \
                      "A.DATA_UPD_ID, " \
                      "A.DATA_UPD_PGM_ID, " \
                      "CASE WHEN A.KD_DIVS_CD = '01' THEN '공지' " \
                      "WHEN A.KD_DIVS_CD = '02' THEN '복리' " \
                      "WHEN A.KD_DIVS_CD = '03' THEN '발령'  " \
                      "WHEN A.KD_DIVS_CD = '04' THEN '그룹웨어'  " \
                      "ELSE '' END KD_DIVS_NM  " \
                      "FROM  TB_STTS_POST_MGMT_M A LEFT OUTER JOIN TB_EMP_MGMT B ON A.DATA_INPT_ID = B.EMP_ID " \
                      "WHERE 1=1 " \
                      "AND  post_id = %s "

                logging.debug(sql)
                cursor.execute(sql, postId)

        finally:
            mysql_con.close()

        result1 = cursor.fetchall()

        return result1


class noticePopCnt(Resource):  # Mariadb 연결 진행
    def get(self):
        logging.debug("noticePopCnt start")
        logging.debug(request.get_json())

        logging.debug('---------------SEARCH---------------')
        logging.debug('------------------------------------')

        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT  COUNT(*) AS COUNT " \
                      "FROM  TB_STTS_POST_MGMT_M " \
                      "WHERE 1=1 " \
                      "AND  POP_OPEN_YN = 'Y' " \
                      "AND DATE(NOW()) BETWEEN date(POP_OPEN_DTTM_FROM) AND date(POP_OPEN_DTTM_TO) "

                logging.debug(sql)
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result1 = cursor.fetchall()

        return result1


class noticePopUp(Resource):  # Mariadb 연결 진행
    def get(self):
        logging.debug("noticePopUp start")
        logging.debug(request.get_json())

        logging.debug('---------------SEARCH---------------')
        logging.debug('------------------------------------')

        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT  A.POST_ID, " \
                      "A.TIT, " \
                      "A.CNTN, " \
                      "A.KD_DIVS_CD, " \
                      "A.MJR_YN, " \
                      "A.POP_OPEN_YN, " \
                      "A.DATA_INPT_ID, " \
                      "B.EMP_NAME, " \
                      "DATE_FORMAT(A.DATA_INPT_DTTM, '%Y-%m-%d %H:%i:%s') AS DATA_INPT_DTTM, " \
                      "A.DATA_INPT_PGM_ID, " \
                      "A.DATA_UPD_ID, " \
                      "DATE_FORMAT(A.DATA_UPD_DTTM, '%Y-%m-%d %H:%i:%s') AS DATA_UPD_DTTM, " \
                      "A.DATA_UPD_PGM_ID, " \
                      "CASE WHEN A.KD_DIVS_CD = '01' THEN '공지' " \
                      "WHEN A.KD_DIVS_CD = '02' THEN '복리' " \
                      "WHEN A.KD_DIVS_CD = '03' THEN '발령'  " \
                      "WHEN A.KD_DIVS_CD = '04' THEN '그룹웨어'  " \
                      "ELSE '' END KD_DIVS_NM  " \
                      "FROM  TB_STTS_POST_MGMT_M A LEFT OUTER JOIN TB_EMP_MGMT B ON A.DATA_INPT_ID = B.EMP_ID " \
                      "WHERE 1=1 " \
                      "AND  A.POP_OPEN_YN = 'Y' " \
                      "AND DATE(NOW()) BETWEEN date(A.POP_OPEN_DTTM_FROM) AND date(A.POP_OPEN_DTTM_TO) "

                logging.debug(sql)
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result1 = cursor.fetchall()

        return result1


class noticeMjrCnt(Resource):  # Mariadb 연결 진행
    def get(self):
        logging.debug("noticeMjrCnt start")
        logging.debug(request.get_json())

        logging.debug('---------------SEARCH---------------')
        logging.debug('param X')
        logging.debug('------------------------------------')

        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT COUNT(MJR_YN) AS CNT " \
                      "FROM TB_STTS_POST_MGMT_M " \
                      "WHERE MJR_YN = 'Y' "
                logging.debug(sql)
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result1 = cursor.fetchall()

        return result1

class noticeSave(Resource):
    def post(self):
        logger.info('========app.py noticeSave=========')
        params = request.get_json()
        logger.info(params)

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        type = request.form['type']
        postId = request.form['postId']
        tit = request.form['tit']
        kdDivsCd = request.form['kdDivsCd']
        mjrYn = request.form['mjrYn']
        popOpenYn = request.form['popOpenYn']
        popOpenDttmFrom = request.form['popOpenDttmFrom']
        popOpenDttmTo = request.form['popOpenDttmTo']
        cntn = request.form['cntn']
        dataUpdId = request.form['dataUpdId']
        dataUpdPgmId = request.form['dataUpdPgmId']
        if type == "c":
            dataInptId = request.form['dataInptId']
            dataInptPgmId = request.form['dataInptPgmId']

        #
        logging.debug("====Param data====")
        logging.debug("type = " + type)
        # logging.debug("postId = " + postId)
        logging.debug("tit = " + tit)
        logging.debug("kdDivsCd = " + kdDivsCd)
        logging.debug("mjrYn = " + mjrYn)
        logging.debug("popOpenYn = " + popOpenYn)
        # logging.debug("popOpenDttmFrom = " + popOpenDttmFrom) -> error:must be str, not tuple -> 타입 달라서 오류남
        # logging.debug("popOpenDttmTo = " + popOpenDttmTo) -> error:must be str, not tuple -> 타입 달라서 오류남
        logging.debug("cntn = " + cntn)
        logging.debug("dataUpdId = " + dataUpdId)
        logging.debug("dataUpdPgmId = " + dataUpdPgmId)
        if type == "c":
            logging.debug("dataInptId = " + dataInptId)
            logging.debug("dataInptPgmId = " + dataInptPgmId)
        logging.debug("=====================")



        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)


        logging.debug("save Start")

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                if type == "c":
                    sql = "INSERT INTO	TB_STTS_POST_MGMT_M	(`TIT`, " \
                                                        "`CNTN`, " \
                                                        "`KD_DIVS_CD`, " \
                                                        "`MJR_YN`, " \
                                                        "`POP_OPEN_YN`, " \
                                                        "`POP_OPEN_DTTM_FROM`, " \
                                                        "`POP_OPEN_DTTM_TO`, " \
                                                        "`DATA_INPT_ID`," \
                                                        "`DATA_INPT_DTTM`," \
                                                        "`DATA_INPT_PGM_ID`," \
                                                        "`DATA_UPD_ID`," \
                                                        "`DATA_UPD_DTTM`," \
                                                        "`DATA_UPD_PGM_ID`) "\
                    "VALUES( %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, NOW(), %s)" \

                    logger.info(sql)
                    cursor.execute(sql, (tit, cntn, kdDivsCd, mjrYn, popOpenYn, popOpenDttmFrom, popOpenDttmTo, dataInptId, dataInptPgmId, dataUpdId, dataUpdPgmId))
                    mysql_con.commit()

                elif type == "u":
                    logging.debug('[dili_api] app.py : update')
                    sql = "UPDATE TB_STTS_POST_MGMT_M " \
                        "SET TIT=%s, CNTN=%s, KD_DIVS_CD=%s, MJR_YN=%s, POP_OPEN_YN=%s, POP_OPEN_DTTM_FROM=%s, POP_OPEN_DTTM_TO=%s, DATA_UPD_ID=%s, DATA_UPD_DTTM=NOW(), DATA_UPD_PGM_ID=%s" \
                        "WHERE POST_ID = %s "

                    logger.info(sql)
                    cursor.execute(sql, (tit, cntn, kdDivsCd, mjrYn, popOpenYn, popOpenDttmFrom, popOpenDttmTo, dataUpdId, dataUpdPgmId, postId))
                    mysql_con.commit()

        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been saved successfully"
        }

        return jsonify(retJson)


class noticeDelete(Resource):
    def post(self):
        logger.info('========app.py noticeDelete=========')
        params = request.get_json()
        logger.info(params)

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        postId = request.form['postId']

        #
        logging.debug("====Param data====")
        logging.debug("postId = " + postId)
        logging.debug("=====================")


        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)

        logging.debug("delete Start")

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                    sql = "DELETE FROM    TB_STTS_POST_MGMT_M WHERE POST_ID = " + postId

                    logger.info(sql)
                    cursor.execute(sql)

                    mysql_con.commit()

        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been deleted successfully"
        }

        return jsonify(retJson)


class saveYryApvlReq(Resource):  # Mariadb 연결 진행
    def post(self):

        params = json.loads(request.data)
        logger.info("App Parameters Start")
        logger.info(params)
        logger.info(type(params))
        logger.info("App Parameters End")

        for row in params:
            logger.info("request.form Parameters Start")
            logger.info(row)

            email = row['email']
            apvlReqDivs = row['apvlReqDivs']
            wrkDt = row['wrkDt']
            wrkTme = row['wrkTme']
            wrkReqRsn = row['wrkReqRsn']
            th1AprvStus = row['th1AprvStus']
            th1AprvNm = row['th1AprvNm']
            th2AprvStus = row['th2AprvStus']
            th2AprvNm = row['th2AprvNm']
            emerCtpl = row['emerCtpl']



            # requirements pymysql import 후 커넥트 사용
            mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
            try:
                with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                    # 쿼리문 실행
                    sql1 = "INSERT INTO TB_APVL_REQ_MGMT_M (" \
                          "`EMP_EMAL_ADDR`," \
                          "`APVL_REQ_DIVS`," \
                          "`WRK_DT`," \
                          "`WRK_TME`," \
                          "`WRK_REQ_RSN`," \
                          "`APVL_REQ_DT`," \
                          "`TH1_APRV_STUS`," \
                          "`TH1_APRV_NM`," \
                          "`TH2_APRV_STUS`," \
                          "`TH2_APRV_NM`," \
                          "`APVL_LAST_APRV_DT`," \
                          "`EMER_CTPL`)" \
                          "VALUES( %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, NOW(), %s)"

                    logger.info(sql1)
                    cursor.execute(sql1, (email, apvlReqDivs, wrkDt, wrkTme, wrkReqRsn, th1AprvStus, th1AprvNm, th2AprvStus, th2AprvNm, emerCtpl))

                    sql2 = "INSERT INTO TB_WRK_TM_MGMT_M(" \
                           "`EMP_EMAL_ADDR`," \
                           "`WRK_DT`)" \
                           "VALUES( %s, %s )"

                    logger.info(sql2)
                    cursor.execute(sql2, (email, wrkDt))

                    sql3 = "UPDATE TB_YRY_MGMT_M" \
                           "   SET USE_YRY_DAYS = USE_YRY_DAYS+1" \
                           " WHERE EMP_EMAL_ADDR = %s" \

                    logger.info(sql3)
                    cursor.execute(sql3, (email))

                    mysql_con.commit()
            except Exception as e:
                logger.info("에러!!!!!!!!!!!!!!!!!!!!!!!"+e)
            finally:
                mysql_con.close()

            retJson = {
                "status": 200,
                "msg": "Data has been saved successfully"
            }

        return jsonify(retJson)

class insertStrtTm(Resource):  # Mariadb 연결 진행
    def post(self):

        params = json.loads(request.data)
        logger.info("App Parameters Start")
        logger.info(params['email'])
        logger.info("App Parameters End")

        email = params['email']
        dt = params['dt']
        tm = params['tm']

        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "INSERT INTO TB_WRK_TM_MGMT_M( `EMP_EMAL_ADDR` " \
                      ",`WRK_DT` " \
                      ",`JOB_STRT_TM` " \
                      ") VALUES( %s ,%s ,%s )"
                logger.info(sql)
                cursor.execute(sql, (email, dt, tm))

                mysql_con.commit()

        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been saved successfully"
        }

        return jsonify(retJson)

class updateEndTm(Resource):  # Mariadb 연결 진행
    def post(self):

        params = json.loads(request.data)
        logger.info("App Parameters Start")
        logger.info(params['email'])
        logger.info("App Parameters End")

        email = params['email']
        dt = params['dt']
        tm = params['tm']
        normWrkTm = params['normWrkTm']
        overWrkTm = params['overWrkTm']
        allWrkTm = params['allWrkTm']


        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "UPDATE TB_WRK_TM_MGMT_M " \
                      "   SET JOB_END_TM  = %s " \
                      "      ,NORM_WRK_TM = %s " \
                      "      ,NGHT_WRK_TM = %s " \
                      "      ,ALL_WRK_TM  = %s " \
                      "   WHERE EMP_EMAL_ADDR = %s " \
                      "   AND WRK_DT = %s "
                logger.info(sql)
                cursor.execute(sql, (tm, normWrkTm, overWrkTm, allWrkTm, email, dt))
                mysql_con.commit()

        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been saved successfully"
        }

        return jsonify(retJson)
    
class yryUseDays(Resource): # Mariadb 연결 진행
    def get(self):

        # get data
        data = request.get_json()

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT CASE WHEN ALL_YRY_DAYS = USE_YRY_DAYS THEN 'N'" \
                      "            ELSE 'Y' END USE_YRY_YN  " \
                      "  FROM TB_YRY_MGMT_M" \
                      " WHERE EMP_EMAL_ADDR = '" + data["email"] + "'"
                logging.debug("apvlReqHist SQL문" + sql)
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)

api.add_resource(Hello, '/hello')
api.add_resource(Register, '/register')
api.add_resource(Retrieve, '/retrieve')
api.add_resource(Save, '/save')

api.add_resource(mariatestDB,'/mariatestDB') #api 선언
api.add_resource(wrkTimeInfoByEml,'/wrkTimeInfoByEml') #api 선언
api.add_resource(yryMgmt,'/yryMgmt') #api 선언
api.add_resource(wrkApvlReq,'/wrkApvlReq') #api 선언
api.add_resource(saveApvlReq,'/saveApvlReq') #api 선언
api.add_resource(apvlReqHist,'/apvlReqHist') #api 선언
api.add_resource(apvlReqHistDetl,'/apvlReqHistDetl') #api 선언
api.add_resource(calendarData,'/calendarData') #api 선언
api.add_resource(noticeLst,'/noticeLst') #api 선언
api.add_resource(noticePopCnt,'/noticePopCnt') #api 선언
api.add_resource(noticeOne,'/noticeOne') #api 선언
api.add_resource(noticePopUp,'/noticePopUp') #api 선언
api.add_resource(noticeMjrCnt,'/noticeMjrCnt') #api 선언
api.add_resource(noticeSave,'/noticeSave') #api 선언
api.add_resource(noticeDelete,'/noticeDelete') #api 선언
api.add_resource(empList,'/empList') #api 선언
api.add_resource(empInfo,'/empInfo') #api 선언
api.add_resource(saveYryApvlReq,'/saveYryApvlReq') #api 선언
api.add_resource(weekGridData,'/weekGridData') #api 선언
api.add_resource(apvlInfo,'/apvlInfo') #api 선언
api.add_resource(monthGridData,'/monthGridData') #api 선언
api.add_resource(insertStrtTm,'/insertStrtTm') #api 선언
api.add_resource(updateEndTm,'/updateEndTm') #api 선언
api.add_resource(yryUseDays,'/yryUseDays') #api 선언
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5006, debug=True)