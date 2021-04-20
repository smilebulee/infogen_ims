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

class totalWrktm(Resource): # Mariadb 연결 진행
    def get(self):
        data = request.get_json()

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT (SELECT CONCAT(COUNT(*) * 8)"\
                      "          FROM TB_DT_INFO"\
                      "         WHERE DT LIKE '" + data["dt"] + "%'"\
                      "           AND HLDY_DIVS_CD = '01'"\
                      "           AND DOW_DIVS_CD NOT IN ('01','07')) AS WRK_TOT_TM" \
                      "       ,(SELECT CONCAT(TRUNCATE((COUNT(*) / 7) * 12, 2))" \
                      "          FROM TB_DT_INFO" \
                      "         WHERE DT LIKE '" + data["dt"] + "%') AS EXTN_WRK_PSBL_TM"\
                      "    FROM DUAL"
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

class hldyMgmt(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT DT, HLDY_DIVS_CD, DOW_DIVS_CD"\
                      "    FROM TB_DT_INFO"\
                      "   WHERE 1=1"\
                      "   AND DT = '" + data["dt"] + "'"
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
                    + "       ,NVL(DATE_FORMAT(A.JOB_STRT_TM, '%H:%i'),'-') AS JOB_STRT_TM "\
                    + "       ,NVL(DATE_FORMAT(A.JOB_END_TM, '%H:%i'),'-') AS JOB_END_TM "\
                    + "       ,CONCAT(SUBSTRING(A.NORM_WRK_TM,1,2),':',SUBSTRING(A.NORM_WRK_TM,3,2)) AS NORM_WRK_TM "\
                    + "       ,CONCAT(SUBSTRING(A.ALL_WRK_TM,1,2),':',SUBSTRING(A.ALL_WRK_TM,3,2)) AS ALL_WRK_TM "\
                    + "       ,DATE_FORMAT(SEC_TO_TIME(TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.ALL_WRK_TM,1,2),':',SUBSTRING(A.ALL_WRK_TM,3,2)) ,'%H:%i')) "\
                    + "                   - TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.NORM_WRK_TM,1,2),':',SUBSTRING(A.NORM_WRK_TM,3,2)) ,'%H:%i'))),'%H:%i') AS OVER_WRK_TM " \
                    + "       ,NVL(B.APVL_REQ_DIVS, 'N/A') AS APVL_REQ_DIVS " \
                    + "       ,NVL(B.APVL_REQ_DT, 'N/A') AS APVL_REQ_DT "\
                    + "       ,NVL(B.APVL_LAST_APRV_DT, 'N/A') AS APVL_LAST_APRV_DT "\
                    + "       ,NVL(B.TH1_APRV_STUS, 'N/A') AS TH1_APRV_STUS"\
                    + "       ,NVL(A.REST_TM,'') AS REST_TM"\
                    + "       ,NVL(A.DINN_REST_TM,'') AS DINN_REST_TM"\
                    + "   FROM TB_WRK_TM_MGMT_M A "\
                    + "        LEFT OUTER JOIN TB_APVL_REQ_MGMT_M B"\
                    + "   ON A.WRK_DT = B.WRK_DT "\
                    + "   AND A.EMP_EMAL_ADDR = B.EMP_EMAL_ADDR "\
                    + "  WHERE 1 = 1 "\
                    + "  AND A.EMP_EMAL_ADDR = '" + data["email"] + "' "\
                    + "  AND A.WRK_DT >= '" + data["strtDt"] + "' "\
                    + "  AND A.WRK_DT <= '" + data["endDt"] + "' "\
                    + "  ORDER BY A.WRK_DT"
                logging.debug(sql + "!!!")
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
                    + "       ,NVL(TH1_APRV_STUS, 'N/A') AS TH1_APRV_STUS "\
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
                    + "       ,NVL(DATE_FORMAT(A.JOB_STRT_TM, '%H:%i'),'-') AS JOB_STRT_TM "\
                    + "       ,NVL(DATE_FORMAT(A.JOB_END_TM, '%H:%i'),'-') AS JOB_END_TM "\
                    + "       ,CONCAT(SUBSTRING(A.NORM_WRK_TM,1,2),':',SUBSTRING(A.NORM_WRK_TM,3,2)) AS NORM_WRK_TM "\
                    + "       ,CONCAT(SUBSTRING(A.ALL_WRK_TM,1,2),':',SUBSTRING(A.ALL_WRK_TM,3,2)) AS ALL_WRK_TM "\
                    + "       ,DATE_FORMAT(SEC_TO_TIME(TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.ALL_WRK_TM,1,2),':',SUBSTRING(A.ALL_WRK_TM,3,2)) ,'%H:%i')) "\
                    + "                   - TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.NORM_WRK_TM,1,2),':',SUBSTRING(A.NORM_WRK_TM,3,2)) ,'%H:%i:%S'))),'%H:%i') AS OVER_WRK_TM "\
                    + "       ,NVL(B.APVL_REQ_DIVS, 'N/A') AS APVL_REQ_DIVS "\
                    + "       ,NVL(B.APVL_REQ_DT, 'N/A') AS APVL_REQ_DT "\
                    + "       ,NVL(B.APVL_LAST_APRV_DT, 'N/A') AS APVL_LAST_APRV_DT "\
                    + "       ,NVL(A.REST_TM,'') AS REST_TM "\
                    + "       ,NVL(A.DINN_REST_TM,'') AS DINN_REST_TM "\
                    + "   FROM TB_WRK_TM_MGMT_M A "\
                    + "        LEFT OUTER JOIN TB_APVL_REQ_MGMT_M B"\
                    + "   ON A.WRK_DT = B.WRK_DT "\
                    + "   AND A.EMP_EMAL_ADDR = B.EMP_EMAL_ADDR "\
                    + "  WHERE 1 = 1 " \
                    + "  AND A.EMP_EMAL_ADDR = '" + data["email"] + "' "\
                    + "  AND A.WRK_DT like '"+data["mDt"]+"%' "\
                    + "  ORDER BY A.WRK_DT"
                logging.debug(sql + "???????")
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
                    + "   AND A.WRK_DT LIKE '" + data["dt"] + "%'" \
                    + " GROUP BY A.EMP_EMAL_ADDR"
                logging.debug(sql + "#####")
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
                      "            WHEN NVL(A.HLDY_WRK_TM,'') = 000000 AND NVL(A.NGHT_WRK_TM,'') != 000000 THEN '야간근무' " \
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
        logger.info("saveApvlReq")

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        currReqPopStts = request.form['currReqPopStts']
        email = request.form['email']
        apvlDivs = request.form['apvlDivs']
        apvlReqDivs = request.form['apvlReqDivs']
        wrkDt = request.form['wrkDt']
        jobStrtTm = request.form['jobStrtTm']
        jobEndTm = request.form['jobEndTm']
        wrkTme = request.form['wrkTme']
        wrkReqRsn = request.form['wrkReqRsn']
        th1AprvStus = request.form['th1AprvStus']
        th1AprvNm = request.form['th1AprvNm']
        refNm = request.form['refNm']

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                if currReqPopStts == "register":
                    sql = "INSERT INTO TB_APVL_REQ_MGMT_M (" \
                                                          "`EMP_EMAL_ADDR`," \
                                                          "`APVL_DIVS`," \
                                                          "`APVL_REQ_DIVS`," \
                                                          "`WRK_DT`," \
                                                          "`JOB_STRT_TM`," \
                                                          "`JOB_END_TM`," \
                                                          "`WRK_TME`," \
                                                          "`WRK_REQ_RSN`," \
                                                          "`APVL_REQ_DT`," \
                                                          "`TH1_APRV_STUS`," \
                                                          "`TH1_APRV_NM`," \
                                                          "`REF_NM`," \
                                                          "`APVL_LAST_APRV_DT`)" \
                                                " VALUES (   '" + email + "'"\
                                                          ", '" + apvlDivs + "'"\
                                                          ", '" + apvlReqDivs + "'"\
                                                          ", '" + wrkDt + "'"\
                                                          ", '" + jobStrtTm + "'"\
                                                          ", '" + jobEndTm + "'"\
                                                          ", '" + wrkTme + "'"\
                                                          ", '" + wrkReqRsn + "'"\
                                                          ",      NOW()" \
                                                          ", '" + th1AprvStus + "'"\
                                                          ", '" + th1AprvNm + "'"\
                                                          ", '" + refNm + "'"\
                                                          ",      NOW())"
                if currReqPopStts == "modify":
                    sql = "UPDATE TB_APVL_REQ_MGMT_M " \
                          "   SET JOB_STRT_TM   = '" + jobStrtTm + "' " \
                          "     , JOB_END_TM    = '" + jobEndTm + "' " \
                          "     , WRK_REQ_RSN   = '" + wrkReqRsn + "' " \
                          "     , TH1_APRV_NM   = '" + th1AprvNm + "' " \
                          "     , REF_NM        = '" + refNm + "' " \
                          "     , APVL_UPD_DT   = NOW() " \
                          " WHERE EMP_EMAL_ADDR = '" + email + "' " \
                          "   AND WRK_DT        = '" + wrkDt + "' "

                logger.info(sql)
                cursor.execute(sql)

                mysql_con.commit()

        finally:
            mysql_con.close()

            retJson = {
                "status": 200,
                "msg": "Data has been saved successfully"
            }

        return jsonify(retJson)

class saveApvlAcpt(Resource): # Mariadb 연결 진행
    def post(self):

        params = request.get_json()
        logger.info(params)
        logger.info("saveApvlAcpt")

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        email = request.form['email']
        wrkDt = request.form['wrkDt']
        jobStrtTm = request.form['jobStrtTm']
        jobEndTm = request.form['jobEndTm']
        th1AprvStus = request.form['th1AprvStus']
        th1AprvRsn = request.form['th1AprvRsn']

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = " UPDATE TB_APVL_REQ_MGMT_M " \
                      "    SET TH1_APRV_STUS     = '" + th1AprvStus + "'" \
                      "      , TH1_APRV_RSN      = '" + th1AprvRsn + "'" \
                      "      , TH1_APRV_DT       = NOW() " \
                      "      , APVL_LAST_APRV_DT = NOW() " \
                      "  WHERE EMP_EMAL_ADDR     = '" + email + "' " \
                      "    AND WRK_DT            = '" + wrkDt + "' " \
                      "    AND JOB_STRT_TM       = '" + jobStrtTm + "' " \
                      "    AND JOB_END_TM        = '" + jobEndTm + "' "

                logger.info(sql)
                cursor.execute(sql)

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

        # get data
        apvlReqDtYm = data["apvlReqDtYm"]
        deptCd = data["deptCd"]
        email = data["email"]
        apvlStusDivs = data["apvlStusDivs"]

        logging.debug('--------------- app.py apvlReqHist data ---------------')
        logging.debug('apvlReqDtYm  : ' + apvlReqDtYm)
        logging.debug('deptCd       : ' + deptCd)
        logging.debug('email        : ' + email)
        logging.debug('apvlStusDivs : ' + apvlStusDivs)
        logging.debug('-------------------------------------------------------')

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT B.EMP_NAME " \
                      "     , A.EMP_EMAL_ADDR " \
                      "     , A.TH1_APRV_NM " \
                      "     , NVL(A.WRK_DT,'') WRK_DT " \
                      "     , NVL(A.JOB_STRT_TM, '') JOB_STRT_TM " \
                      "     , NVL(A.JOB_END_TM, '') JOB_END_TM " \
                      "     , CASE WHEN A.APVL_REQ_DIVS = '01' THEN NVL(A.WRK_TME,'') " \
                      "            WHEN A.APVL_REQ_DIVS = '02' THEN NVL(A.WRK_TME,'') " \
                      "            ELSE '' END WRK_TME  " \
                      "     , CASE WHEN A.APVL_REQ_DIVS = '01' THEN '야간근무' " \
                      "            WHEN A.APVL_REQ_DIVS = '02' THEN '휴일근무' " \
                      "            WHEN A.APVL_REQ_DIVS = '03' THEN '연차결재'  " \
                      "            ELSE '' END APVL_REQ_NM  " \
                      "     , CASE WHEN A.TH1_APRV_STUS = '01' THEN '미승인'" \
                      "            WHEN A.TH1_APRV_STUS = '02' THEN '승인'" \
                      "            ELSE '반려' END APRV_STUS_NM" \
                      "     , A.TH1_APRV_STUS" \
                      "     , C.EMP_NAME AS REF_NM" \
                      "     , A.APVL_REQ_DT" \
                      "     , A.WRK_REQ_RSN" \
                      "  FROM TB_APVL_REQ_MGMT_M A, TB_EMP_MGMT B, TB_EMP_MGMT C" \
                      " WHERE A.EMP_EMAL_ADDR = B.EMP_EMAIL" \
                      "   AND A.TH1_APRV_NM = C.EMP_EMAIL " \
                      "   AND A.APVL_REQ_DT LIKE '" + apvlReqDtYm + "%' "
                if apvlStusDivs != "" and apvlStusDivs != "00": #미승인, 승인, 반려
                    sql += "   AND A.TH1_APRV_STUS = '" + apvlStusDivs + "' "
                if email != "":
                    sql += "   AND A.EMP_EMAL_ADDR = '" + email + "' "
                if deptCd != "" and deptCd != "00":
                    sql += "   AND B.DEPT_CD = '" + deptCd + "' "

                sql += " ORDER BY A.APVL_REQ_DT ASC "
                logging.debug("apvlReqHist SQL문" + sql)
                cursor.execute(sql)


        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row ====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)


class apvlAcptHist(Resource):  # Mariadb 연결 진행
    def get(self):

        # get data
        data = request.get_json()

        # get data
        email = data["email"]
        apvlStusDivs = data["apvlStusDivs"]

        logging.debug('--------------- app.py apvlAcptHist data ---------------')
        logging.debug('email : '        + email)
        logging.debug('apvlStusDivs : ' + apvlStusDivs)
        logging.debug('------------------------------------')

        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                if apvlStusDivs == "00":
                    # 전체
                    sql = "SELECT A.EMP_EMAL_ADDR, C.EMP_NAME " \
                          "     , NVL(A.WRK_DT,'') WRK_DT " \
                          "     , NVL(A.JOB_STRT_TM, '') JOB_STRT_TM " \
                          "     , NVL(A.JOB_END_TM, '') JOB_END_TM " \
                          "     , CASE WHEN A.APVL_REQ_DIVS = '01' THEN NVL(A.WRK_TME,'') WHEN A.APVL_REQ_DIVS = '02' THEN NVL(A.WRK_TME,'') ELSE '' END WRK_TME  " \
                          "     , CASE WHEN A.APVL_REQ_DIVS = '01' THEN '야간근무' WHEN A.APVL_REQ_DIVS = '02' THEN '휴일근무' WHEN A.APVL_REQ_DIVS = '03' THEN '연차결재' ELSE '' END APVL_REQ_NM  " \
                          "     , CASE WHEN A.TH1_APRV_STUS = '01' THEN '미승인'  " \
                          "       	   WHEN A.TH1_APRV_STUS = '02' THEN '승인'  " \
                          "            ELSE '반려' END APRV_STUS_NM " \
                          "     , NVL(A.APVL_REQ_DT, '') APVL_REQ_DT " \
                          "     , NVL(A.WRK_REQ_RSN, '') WRK_REQ_RSN " \
                          "     , A.TH1_APRV_STUS" \
                          "  FROM TB_APVL_REQ_MGMT_M A, TB_EMP_MGMT B, TB_EMP_MGMT C " \
                          " WHERE A.EMP_EMAL_ADDR = C.EMP_EMAIL  " \
                          "   AND A.TH1_APRV_NM = B.EMP_EMAIL  " \
                          "   AND A.TH1_APRV_NM = '" + email + "' " \
                          " ORDER BY APVL_REQ_DT ASC "

                    logging.debug("apvlAcptHist SQL문" + sql)
                    cursor.execute(sql)

                if apvlStusDivs != "00":
                    # 미승인, 승인, 반려
                    sql = "SELECT A.EMP_EMAL_ADDR, C.EMP_NAME " \
                          "     , NVL(A.WRK_DT,'') WRK_DT " \
                          "     , NVL(A.JOB_STRT_TM, '') JOB_STRT_TM " \
                          "     , NVL(A.JOB_END_TM, '') JOB_END_TM " \
                          "     , CASE WHEN A.APVL_REQ_DIVS = '01' THEN NVL(A.WRK_TME,'') WHEN A.APVL_REQ_DIVS = '02' THEN NVL(A.WRK_TME,'') ELSE '' END WRK_TME  " \
                          "     , CASE WHEN A.APVL_REQ_DIVS = '01' THEN '야간근무' WHEN A.APVL_REQ_DIVS = '02' THEN '휴일근무' WHEN A.APVL_REQ_DIVS = '03' THEN '연차결재' ELSE '' END APVL_REQ_NM  " \
                          "     , CASE WHEN A.TH1_APRV_STUS = '01' THEN '미승인'  " \
                          "       	   WHEN A.TH1_APRV_STUS = '02' THEN '승인'  " \
                          "            ELSE '반려' END APRV_STUS_NM " \
                          "     , NVL(A.APVL_REQ_DT, '') APVL_REQ_DT " \
                          "     , NVL(A.WRK_REQ_RSN, '') WRK_REQ_RSN " \
                          "     , A.TH1_APRV_STUS" \
                          "  FROM TB_APVL_REQ_MGMT_M A, TB_EMP_MGMT B, TB_EMP_MGMT C " \
                          " WHERE A.EMP_EMAL_ADDR = C.EMP_EMAIL  " \
                          "   AND A.TH1_APRV_NM = B.EMP_EMAIL  " \
                          "   AND A.TH1_APRV_NM = '" + email + "' " \
                          "   AND A.TH1_APRV_STUS = '" + apvlStusDivs + "' " \
                          " ORDER BY APVL_REQ_DT ASC "

                    logging.debug("apvlAcptHist SQL문" + sql)
                    cursor.execute(sql)

        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row ====')
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
        workChk = data["workChk"]

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
                if workChk == 'Y':
                    #현재 재직중인 직원 조회
                    sql = "SELECT SEQ_NO, EMP_NAME, EMP_EMAIL, EMP_ID, AUTH_ID AUTH_VAL, DEPT_CD, DEPT_NAME, WORK_YN " \
                          "FROM TB_EMP_MGMT " \
                          "WHERE EMP_NAME LIKE '%" + data["name"] + "%' " \
                          "AND WORK_YN = 'Y' " \
                          "ORDER BY SEQ_NO"

                else:
                    # 전체 직원 조회
                    sql = "SELECT SEQ_NO, EMP_NAME, EMP_EMAIL, EMP_ID, AUTH_ID AUTH_VAL, DEPT_CD, DEPT_NAME, WORK_YN " \
                          "FROM TB_EMP_MGMT " \
                          "WHERE EMP_NAME LIKE '%" + data["name"] + "%' " \
                          "ORDER BY SEQ_NO"

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


class empName(Resource): # Mariadb 연결 진행
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
                sql = "SELECT EMP_NAME FROM TB_EMP_MGMT WHERE EMP_EMAIL = '" + data["email"] + "'"

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


class empDeptGm(Resource): # Mariadb 연결 진행
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
                sql = "SELECT DEPT_CD " \
                      "     , DEPT_NAME " \
                      "     , EMP_NAME AS DEPT_GM_NAME " \
                      "     , EMP_EMAIL AS DEPT_GM_EMAIL " \
                      "  FROM TB_EMP_MGMT " \
                      " WHERE AUTH_ID LIKE '%GM%'" \
                      "   AND DEPT_CD = (" \
                      "                  SELECT DEPT_CD " \
                      "                    FROM TB_EMP_MGMT " \
                      "                   WHERE EMP_EMAIL = '" + data["email"] + "'" \
                      "                 )"

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


class empDeptPr(Resource): # Mariadb 연결 진행
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
                sql = "SELECT DEPT_CD " \
                      "     , DEPT_NAME " \
                      "     , EMP_NAME AS DEPT_PR_NAME " \
                      "     , EMP_EMAIL AS DEPT_PR_EMAIL " \
                      "  FROM TB_EMP_MGMT " \
                      " WHERE AUTH_ID LIKE '%PR%'" \
                      "   AND DEPT_CD = (" \
                      "                  SELECT DEPT_CD " \
                      "                    FROM TB_EMP_MGMT " \
                      "                   WHERE EMP_EMAIL = '" + data["email"] + "'" \
                      "                 )"

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


class empDept(Resource): # Mariadb 연결 진행
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
                sql = "SELECT DEPT_CD " \
                      "     , DEPT_NAME " \
                      "  FROM TB_EMP_MGMT " \
                      " WHERE EMP_EMAIL = '" + data["email"] + "'"

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


class duplApvlReqCnt(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT COUNT(*) AS APVL_REQ_CNT " \
                      "  FROM TB_APVL_REQ_MGMT_M " \
                      " WHERE EMP_EMAL_ADDR = '" + data["email"] + "' " \
                      "   AND WRK_DT = '" + data["wrkDt"] + "' "
                logging.debug("duplApvlReqCnt SQL문" + sql)
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
                sql = "            SELECT NVL(A.EMP_EMAL_ADDR,'') EMP_EMAIL " \
                      "                 , NVL(D.EMP_NAME,'') EMP_NAME " \
                      "                 , A.TH1_APRV_NM TH1_APRV_NM " \
                      "                 , NVL(B.EMP_NAME,'') TH1_APRV_NAME " \
                      "                 , NVL(C.EMP_EMAIL,'') REF_NM" \
                      "                 , NVL(C.EMP_NAME,'') REF_NAME" \
                      "                 , DATE_FORMAT(A.APVL_REQ_DT, '%Y-%m-%d') APVL_REQ_DT" \
                      "                 , DATE_FORMAT(A.WRK_DT, '%Y-%m-%d') WRK_DT" \
                      "                 , DATE_FORMAT(A.JOB_STRT_TM, '%H:%i:%s') JOB_STRT_TM" \
                      "                 , DATE_FORMAT(A.JOB_END_TM, '%H:%i:%s') JOB_END_TM" \
                      "                 , A.WRK_REQ_RSN" \
                      "                 , NVL(DATE_FORMAT(A.APVL_UPD_DT, '%Y-%m-%d'), '') APVL_UPD_DT" \
                      "                 , NVL(A.TH1_APRV_RSN,'') TH1_APRV_RSN " \
                      "                 , NVL(DATE_FORMAT(A.TH1_APRV_DT, '%Y-%m-%d'), '') TH1_APRV_DT" \
                      "              FROM TB_APVL_REQ_MGMT_M A " \
                      "   LEFT OUTER JOIN TB_EMP_MGMT B " \
                      "                ON A.TH1_APRV_NM = B.EMP_EMAIL " \
                      "   LEFT OUTER JOIN TB_EMP_MGMT C " \
                      "                ON A.REF_NM = C.EMP_EMAIL " \
                      "   LEFT OUTER JOIN TB_EMP_MGMT D " \
                      "                ON A.EMP_EMAL_ADDR = D.EMP_EMAIL " \
                      "             WHERE A.EMP_EMAL_ADDR = '" + data["email"]     + "'" \
                      "               AND A.WRK_DT = '"        + data["wrkDt"]     + "'"
                logging.debug("apvlReqHistDetl SQL문" + sql)
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
                      + "       ,NVL(DATE_FORMAT(A.JOB_STRT_TM, '%H:%i'),'-') AS JOB_STRT_TM " \
                      + "       ,NVL(DATE_FORMAT(A.JOB_END_TM, '%H:%i'),'-') AS JOB_END_TM " \
                      + "       ,A.NORM_WRK_TM " \
                      + "       ,A.ALL_WRK_TM " \
                      + "       ,NVL(B.APVL_REQ_DIVS, 'N/A') AS APVL_REQ_DIVS " \
                      + "       ,NVL(B.APVL_REQ_DT, 'N/A') AS APVL_REQ_DT " \
                      + "       ,NVL(B.APVL_LAST_APRV_DT, 'N/A') AS APVL_LAST_APRV_DT " \
                      + "       ,NVL(B.TH1_APRV_STUS, 'N/A') AS TH1_APRV_STUS " \
                      + "       ,DATE_FORMAT(SEC_TO_TIME(TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.ALL_WRK_TM,1,2),':',SUBSTRING(A.ALL_WRK_TM,3,2)) ,'%H:%i')) " \
                      + "                   - TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.NORM_WRK_TM,1,2),':',SUBSTRING(A.NORM_WRK_TM,3,2)) ,'%H:%i'))),'%H:%i') AS OVER_WRK_TM " \
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
                           "`APVL_LAST_APRV_DT`," \
                           "`EMER_CTPL`)" \
                           "VALUES( %s, %s, %s, %s, %s, NOW(), %s, %s, NOW(), %s)"

                    logger.info(sql1)
                    cursor.execute(sql1, (email, apvlReqDivs, wrkDt, wrkTme, wrkReqRsn, th1AprvStus, th1AprvNm, emerCtpl))

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
        logger.info("email" + params['email'])
        logger.info("dt" + params['dt'])
        logger.info("tm" + params['tm'])
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
                      ") VALUES( %s ,%s ,%s ) " \
                      "ON DUPLICATE KEY " \
                      "UPDATE `JOB_STRT_TM` = %s"
                logger.info(sql)
                cursor.execute(sql, (email, dt, tm, tm))

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
                if normWrkTm == "000000" and allWrkTm != "000000":
                    # 쿼리문 실행
                    sql = "UPDATE TB_WRK_TM_MGMT_M " \
                          "   SET JOB_END_TM  = %s " \
                          "      ,HLDY_WRK_TM = %s " \
                          "      ,ALL_WRK_TM  = %s " \
                          "   WHERE EMP_EMAL_ADDR = %s " \
                          "   AND WRK_DT = %s "
                    logger.info(sql)
                    cursor.execute(sql, (tm, overWrkTm, allWrkTm, email, dt))
                    mysql_con.commit()
                else:
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
                logging.debug("yryUseDays SQL문" + sql)
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

#공통 코드 조회
class retrieveCmmCd(Resource):
    def get(self):
        logging.debug('retrieveCmmCd Start')

        # get data
        data = request.get_json()

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT " \
                      "CMM_CD_GRP_ID, CMM_CD, CMM_CD_NAME " \
                      "FROM TB_CMM_CD_DETL A " \
                      "WHERE CMM_CD_GRP_ID = '" + data["grp_id"] + "'"
                cursor.execute(sql)
                logging.debug('retrieveCmmCd SUCCESS')
        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)

class scheduleStatLst(Resource):
    def get(self):

        logging.debug('scheduleStatLst Start')

        # get data
        data = request.get_json()

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT CASE WHEN NVL(B.EMP_EMAL_ADDR, '') = '' THEN A.EMP_EMAL_ADDR" \
                      "            WHEN NVL(A.EMP_EMAL_ADDR, '') = '' THEN B.EMP_EMAL_ADDR" \
                      "                                               ELSE A.EMP_EMAL_ADDR" \
                      "                                                END EMP_EMAL_ADDR" \
                      "      ,CASE WHEN NVL(B.WRK_DT, '') = '' THEN A.WRK_DT" \
                      "            WHEN NVL(A.WRK_DT, '') = '' THEN B.WRK_DT" \
                      "                                        ELSE A.WRK_DT" \
                      "                                         END WRK_DT" \
                      "      ,(SELECT D.CMM_CD_NAME" \
                      "		     FROM TB_CMM_CD_DETL D" \
                      "		         ,TB_EMP_MGMT E" \
                      "			WHERE D.CMM_CD_GRP_ID = 'SLIN_BZDP'" \
                      "			  AND D.CMM_CD = E.DEPT_CD" \
                      "			  AND E.EMP_EMAIL = NVL(A.EMP_EMAL_ADDR, B.EMP_EMAL_ADDR)) DEPT_NAME" \
                      "	     ,(SELECT C.EMP_NAME " \
                      "	         FROM TB_EMP_MGMT C" \
                      "	        WHERE C.EMP_EMAIL = NVL(A.EMP_EMAL_ADDR, B.EMP_EMAL_ADDR)) OCEM_NAME" \
                      "      ,CASE WHEN B.EMP_EMAL_ADDR IS NULL AND (A.HLDY_WRK_TM != '000000' OR A.NGHT_WRK_TM != '000000') THEN '야근(미승인)'" \
                      "            WHEN B.APVL_REQ_DIVS IS NOT NULL THEN (SELECT F.CMM_CD_NAME" \
                      "                                                     FROM TB_CMM_CD_DETL F" \
                      "      										       WHERE F.CMM_CD_GRP_ID = 'APVL_DIVS_CD'" \
                      "      				     						     AND F.CMM_CD = B.APVL_REQ_DIVS)" \
                      "      		ELSE '정상근무' END WRK_DIVS" \
                      "		 ,(SELECT NVL((SELECT F.CMM_CD_NAME" \
                      "                      FROM TB_CMM_CD_DETL F" \
                      "                     WHERE F.CMM_CD_GRP_ID = 'APVL_STTS_CD'" \
                      "                       AND F.CMM_CD = B.TH1_APRV_STUS), '')" \
                      "          FROM DUAL) APVL_STUS" \
                      "		 ,CASE WHEN NVL(B.APVL_REQ_DIVS, '') = '' THEN NVL(A.JOB_STRT_TM, '')" \
                      "		       WHEN B.APVL_REQ_DIVS = '01' OR B.APVL_REQ_DIVS = '02'" \
                      "		       THEN NVL(B.JOB_STRT_TM, '') ELSE '' END WRK_STRT_TM" \
                      "		 ,CASE WHEN NVL(B.APVL_REQ_DIVS, '') = '' THEN NVL(A.JOB_END_TM, '')" \
                      "		       WHEN B.APVL_REQ_DIVS = '01' OR B.APVL_REQ_DIVS = '02'" \
                      "		       THEN NVL(B.JOB_END_TM, '') ELSE '' END WRK_END_TM" \
                      "		 ,NVL(A.ALL_WRK_TM,'') ALL_WRK_TM" \
                      "      ,CASE WHEN B.EMP_EMAL_ADDR IS NULL AND (A.HLDY_WRK_TM != '000000' OR A.NGHT_WRK_TM != '000000') THEN 'N'" \
                      "            ELSE 'Y' END APVL_REQ_YN" \
                      "  FROM TB_WRK_TM_MGMT_M A" \
                      "  LEFT OUTER JOIN" \
                      "       TB_APVL_REQ_MGMT_M B" \
                      "    ON A.EMP_EMAL_ADDR = B.EMP_EMAL_ADDR" \
                      "   AND A.WRK_DT = B.WRK_DT" \
                      " WHERE SUBSTRING(A.WRK_DT, 1, 7) = '" + data["wrkDt"] + "'"
                if data["email"] != "":
                      sql += "    AND A.EMP_EMAL_ADDR = '" + data["email"] + "'" \

                if data["apvlStus"] != "" and data["apvlStus"] != "00":
                      sql += "    AND B.TH1_APRV_STUS = '" + data["apvlStus"] + "'" \

                if data["wrkDivs"] != "" and data["wrkDivs"] != "00" and data["wrkDivs"] != "04" and data["wrkDivs"] != "05":
                      sql += "    AND B.APVL_REQ_DIVS = '" + data["wrkDivs"] + "'" \

                if data["wrkDivs"] != "" and data["wrkDivs"] == "04":
                      sql += "    AND A.HLDY_WRK_TM = '000000'" \
                             "    AND A.NGHT_WRK_TM = '000000'" \
                             "    AND A.ALL_WRK_TM != '000000'" \
                    
                if data["wrkDivs"] != "" and data["wrkDivs"] == "05":
                      sql += "    AND B.EMP_EMAL_ADDR IS NULL" \
                             "    AND (A.HLDY_WRK_TM != '000000' OR A.NGHT_WRK_TM != '000000')" \

                if data["dept"] != "" and data["dept"] != "00":
                      sql += "    AND A.EMP_EMAL_ADDR IN (SELECT H.EMP_EMAIL" \
                             "                              FROM TB_EMP_MGMT H" \
                             "                             WHERE H.DEPT_CD = '" + data["dept"] + "')" \

                sql +=" UNION" \
                      " SELECT CASE WHEN NVL(A.EMP_EMAL_ADDR, '') = '' THEN B.EMP_EMAL_ADDR" \
                      "             WHEN NVL(B.EMP_EMAL_ADDR, '') = '' THEN A.EMP_EMAL_ADDR" \
                      "				                                   ELSE B.EMP_EMAL_ADDR" \
                      "													END EMP_EMAL_ADDR" \
                      "		  ,CASE WHEN NVL(A.WRK_DT, '') = '' THEN B.WRK_DT" \
                      "             WHEN NVL(B.WRK_DT, '') = '' THEN A.WRK_DT" \
                      "				                            ELSE B.WRK_DT" \
                      "							  			     END WRK_DT" \
                      "		  ,(SELECT D.CMM_CD_NAME" \
                      "		      FROM TB_CMM_CD_DETL D" \
                      "		          ,TB_EMP_MGMT E" \
                      "			 WHERE D.CMM_CD_GRP_ID = 'SLIN_BZDP'" \
                      "			   AND D.CMM_CD = E.DEPT_CD" \
                      "			   AND E.EMP_EMAIL = NVL(A.EMP_EMAL_ADDR, B.EMP_EMAL_ADDR)) DEPT_NAME" \
                      "		  ,(SELECT C.EMP_NAME" \
                      "	          FROM TB_EMP_MGMT C" \
                      "	         WHERE C.EMP_EMAIL = NVL(A.EMP_EMAL_ADDR, B.EMP_EMAL_ADDR)) OCEM_NAME" \
                      "      ,CASE WHEN B.EMP_EMAL_ADDR IS NULL AND (A.HLDY_WRK_TM != '000000' OR A.NGHT_WRK_TM != '000000') THEN '야근(미승인)'" \
                      "            WHEN B.APVL_REQ_DIVS IS NOT NULL THEN (SELECT F.CMM_CD_NAME" \
                      "                                                     FROM TB_CMM_CD_DETL F" \
                      "      										       WHERE F.CMM_CD_GRP_ID = 'APVL_DIVS_CD'" \
                      "      				     						     AND F.CMM_CD = B.APVL_REQ_DIVS)" \
                      "      		ELSE '정상근무' END WRK_DIVS" \
                      "		 ,(SELECT NVL((SELECT F.CMM_CD_NAME" \
                      "                      FROM TB_CMM_CD_DETL F" \
                      "                     WHERE F.CMM_CD_GRP_ID = 'APVL_STTS_CD'" \
                      "                       AND F.CMM_CD = B.TH1_APRV_STUS), '')" \
                      "          FROM DUAL) APVL_STUS" \
                      "		 ,CASE WHEN NVL(B.APVL_REQ_DIVS, '') = '' THEN NVL(A.JOB_STRT_TM, '')" \
                      "		       WHEN B.APVL_REQ_DIVS = '01' OR B.APVL_REQ_DIVS = '02'" \
                      "		       THEN NVL(B.JOB_STRT_TM, '') ELSE '' END WRK_STRT_TM" \
                      "		 ,CASE WHEN NVL(B.APVL_REQ_DIVS, '') = '' THEN NVL(A.JOB_END_TM, '')" \
                      "		       WHEN B.APVL_REQ_DIVS = '01' OR B.APVL_REQ_DIVS = '02'" \
                      "		       THEN NVL(B.JOB_END_TM, '') ELSE '' END WRK_END_TM" \
                      "		 ,NVL(B.WRK_TME,'') ALL_WRK_TM" \
                      "      ,CASE WHEN B.EMP_EMAL_ADDR IS NULL AND (A.HLDY_WRK_TM != '000000' OR A.NGHT_WRK_TM != '000000') THEN 'N'" \
                      "            ELSE 'Y' END APVL_REQ_YN" \
                      "   FROM TB_WRK_TM_MGMT_M A" \
                      "  RIGHT OUTER JOIN" \
                      "        TB_APVL_REQ_MGMT_M B" \
                      "     ON A.EMP_EMAL_ADDR = B.EMP_EMAL_ADDR" \
                      "    AND A.WRK_DT = B.WRK_DT" \
                      "  WHERE SUBSTRING(B.WRK_DT, 1, 7) = '" + data["wrkDt"] + "'"
                if data["email"] != "":
                      sql += "    AND B.EMP_EMAL_ADDR = '" + data["email"] + "'" \

                if data["apvlStus"] != "" and data["apvlStus"] != "00":
                      sql += "    AND B.TH1_APRV_STUS = '" + data["apvlStus"] + "'" \

                if data["wrkDivs"] != "" and data["wrkDivs"] != "00" and data["wrkDivs"] != "04" and data["wrkDivs"] != "05":
                      sql += "    AND B.APVL_REQ_DIVS = '" + data["wrkDivs"] + "'" \
                    
                if data["wrkDivs"] != "" and data["wrkDivs"] == "04":
                      sql += "    AND A.HLDY_WRK_TM = '000000'" \
                             "    AND A.NGHT_WRK_TM = '000000'" \
                             "    AND A.ALL_WRK_TM != '000000'" \

                if data["wrkDivs"] != "" and data["wrkDivs"] == "05":
                      sql += "    AND B.EMP_EMAL_ADDR IS NULL" \
                             "    AND (A.HLDY_WRK_TM != '000000' OR A.NGHT_WRK_TM != '000000')" \
                
                if data["dept"] != "" and data["dept"] != "00":
                      sql += "    AND B.EMP_EMAL_ADDR IN (SELECT H.EMP_EMAIL" \
                             "                              FROM TB_EMP_MGMT H" \
                             "                             WHERE H.DEPT_CD = '" + data["dept"] + "')"
                logging.debug(sql)
                cursor.execute(sql)
                logging.debug('scheduleStatLst SUCCESS')
        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)

class empMgmtRegSubmit(Resource):
    def post(self):
        logger.info('========app.py empMgmtRegSubmit=========')
        params = request.get_json()
        logger.info(params)

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        ipt_empId = request.form['ipt_empId']
        ipt_empPw = request.form['ipt_empPw']
        ipt_empAuthId = request.form['ipt_empAuthId']
        ipt_empNm = request.form['ipt_empNm']
        ipt_empDept = request.form['ipt_empDept']
        sessionId = request.form['sessionId']
        ipt_empEmail = ipt_empId;


        logging.debug("====Param data====")

        logging.debug("ipt_empId = " + ipt_empId)
        logging.debug("ipt_empEmail = " + ipt_empEmail)
        logging.debug("ipt_empPw = " + ipt_empPw)
        logging.debug("ipt_empAuthId = " + ipt_empAuthId)
        logging.debug("ipt_empNm = " + ipt_empNm)
        logging.debug("ipt_empDept = " + ipt_empDept)
        logging.debug("sessionId = " + sessionId)


        logging.debug("=====================")



        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)


        logging.debug("save Start")

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql= "INSERT INTO TB_EMP_MGMT (EMP_ID, " \
                                                "EMP_EMAIL, " \
                                                "EMP_PW, " \
                                                "EMP_NAME, " \
                                                "AUTH_ID, " \
                                                "REG_DTM, " \
                                                "REG_USER, " \
                                                "WORK_YN, " \
                                                "DEPT_CD, " \
                                                "DEPT_NAME) " \
                                    "VALUES('" + ipt_empId + "', " \
                                            "'" + ipt_empEmail + "', " \
                                            "'" + ipt_empPw + "', " \
                                            "'" + ipt_empNm + "', " \
                                            "'" + ipt_empAuthId + "', " \
                                            "now(), " \
                                            "'" + sessionId + "', " \
                                            "'Y', " \
                                            "'" + ipt_empDept + "', " \
                                            "(SELECT CMM_CD_NAME DEPT_VAL FROM TB_CMM_CD_DETL WHERE CMM_CD_GRP_ID = 'SLIN_BZDP' AND CMM_CD = " \
                                            "'" + ipt_empDept + "'))"\

                logger.info(sql)
                cursor.execute(sql)
                mysql_con.commit()

        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been saved successfully"
        }

        return jsonify(retJson)


class empOneInfo(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        logging.debug('================== App Start ==================')
        logging.debug(data)
        logging.debug(data["email"])
        logging.debug(request.args.get('email'))
        logging.debug(request.args.get('param'))
        logging.debug('================== App End ==================')

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT EMP_ID, EMP_PW, AUTH_ID, EMP_NAME, DEPT_CD FROM TB_EMP_MGMT WHERE EMP_EMAIL = '" + data["email"] + "'"

                logging.debug(sql)
                cursor.execute(sql)
                logging.debug('getEditEmpInfo SUCCESS')

        finally:
            mysql_con.close()
            logging.debug('getEditEmpInfo CLOSE')



        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)

class isExistEmpNm(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

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
                sql = "SELECT EMP_ID, EMP_PW, AUTH_ID, EMP_NAME, DEPT_CD FROM TB_EMP_MGMT WHERE EMP_NAME = '" + data["name"] + "'"

                logging.debug(sql)
                cursor.execute(sql)
                logging.debug('getEditEmpInfo SUCCESS')

        finally:
            mysql_con.close()
            logging.debug('getEditEmpInfo CLOSE')



        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)

class empMgmtEditSubmit(Resource):
    def post(self):
        logger.info('========app.py empMgmtEditSubmit=========')
        params = request.get_json()
        logger.info(params)

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        ipt_empId = request.form['ipt_empId']
        ipt_empPw = request.form['ipt_empPw']
        ipt_empAuthId = request.form['ipt_empAuthId']
        ipt_empNm = request.form['ipt_empNm']
        ipt_empDept = request.form['ipt_empDept']
        sessionId = request.form['sessionId']
        ipt_empEmail = ipt_empId;


        logging.debug("====Param data====")

        logging.debug("ipt_empId = " + ipt_empId)
        logging.debug("ipt_empEmail = " + ipt_empEmail)
        logging.debug("ipt_empPw = " + ipt_empPw)
        logging.debug("ipt_empAuthId = " + ipt_empAuthId)
        logging.debug("ipt_empNm = " + ipt_empNm)
        logging.debug("ipt_empDept = " + ipt_empDept)
        logging.debug("sessionId = " + sessionId)

        logging.debug("=====================")



        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)


        logging.debug("save Start")

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql= "UPDATE TB_EMP_MGMT SET EMP_PW = '"+ipt_empPw+"', " \
                                                "EMP_NAME = '"+ipt_empNm+"', " \
                                                "AUTH_ID = '"+ipt_empAuthId+"', " \
                                                "DEPT_CD = '"+ipt_empDept+"', " \
                                                "UPD_DTM = now(), " \
                                                "UPD_USER = '"+sessionId+"', " \
                                                "DEPT_NAME = (SELECT CMM_CD_NAME DEPT_VAL FROM TB_CMM_CD_DETL WHERE CMM_CD_GRP_ID = 'SLIN_BZDP' AND CMM_CD = '" + ipt_empDept + "') " \
                                                "WHERE EMP_ID = '"+ipt_empId+"'" \

                logger.info(sql)
                cursor.execute(sql)
                mysql_con.commit()

        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been saved successfully"
        }

        return jsonify(retJson)

class empMgmtDelSubmit(Resource):
    def post(self):
        logger.info('========app.py empMgmtDelSubmit=========')
        params = request.get_json()
        logger.info(params)

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        ipt_empId = request.form['ipt_empId']

        logging.debug("====Param data====")

        logging.debug("ipt_empId = " + ipt_empId)

        logging.debug("=====================")



        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)


        logging.debug("save Start")

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql= "UPDATE TB_EMP_MGMT SET WORK_YN ='N', " \
                                            "UPD_DTM = now(), " \
                                            "UPD_USER = '"+sessionId+"' " \
                                            "WHERE EMP_ID = '"+ipt_empId+"'"

                logger.info(sql)
                cursor.execute(sql)
                mysql_con.commit()

        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been saved successfully"
        }

        return jsonify(retJson)

class question(Resource):  # Mariadb 연결 진행
    def get(self):
        logging.debug('---------------QnA---------------')
        logging.debug(request.get_json())

        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT  * " \
                      "FROM  TB_QNA_TEST " \
                      "WHERE QNA_DEL_YN = 'N' " \
                      "ORDER BY QNA_ORIGIN_NO DESC, QNA_SORTS "


                logging.debug(sql)
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result1 = cursor.fetchall()

        return result1


class questionInfo(Resource):  # Mariadb 연결 진행
    def get(self):
        data =request.get_json()

        logging.debug('================== App Start ==================')
        logging.debug(data)
        logging.debug(data["name"])
        logging.debug(request.args.get('name'))
        logging.debug(request.args.get('param'))
        logging.debug('================== App End ==================')

        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:

                sql = "SELECT A.QNA_WR_NM ORIGIN_WR, B.QNA_NO,  B.QNA_ORIGIN_NO,  B.DATA_DEPTH, B.QNA_SORTS, B.QNA_TITLE,  B.QNA_MAIN,  B.QNA_WR_NM , B.QNA_RGS_DATE, B.QNA_DEL_YN " \
                      "FROM TB_QNA_TEST  A, TB_QNA_TEST B " \
                      "WHERE A.QNA_NO = B.QNA_ORIGIN_NO AND B.QNA_ORIGIN_NO NOT IN (SELECT QNA_NO FROM TB_QNA_TEST WHERE DATA_DEPTH = 0 AND QNA_DEL_YN = 'Y') " \
                      "ORDER BY B.QNA_ORIGIN_NO DESC, B.QNA_SORTS ASC"

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

class qnaPopCnt(Resource):  # Mariadb 연결 진행
    def get(self):
        logging.debug(request.get_json())

        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT  COUNT(*) AS COUNT " \
                      "FROM TB_QNA_TEST " \
                      "WHERE QNA_DEL_YN = 'N' " \
                      "ORDER BY QNA_ORIGIN_NO DESC, QNA_SORTS"

                logging.debug(sql)
                cursor.execute(sql)

        finally:
            mysql_con.close()
        result1 = cursor.fetchall()
        return result1


class qnaPopUp(Resource):  # Mariadb 연결 진행
    def get(self):
        logging.debug("qnaPopUp start")
        logging.debug(request.get_json())


        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT  QNA_TITLE,  QNA_WR_NM,  QNA_RGS_DATE, QNA_DEL_YN" \
                      "FROM TB_QNA_TEST " \
                      "ORDER BY QNA_ORIGIN_NO DESC, QNA_SORTS"

                logging.debug(sql)
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result1 = cursor.fetchall()

        return result1


class questionWrSubmit(Resource):
    def post(self):
        params = request.get_json()
        logger.info(params)

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        ipt_wrId = request.form['ipt_wrId']
        ipt_qnatitle = request.form['ipt_qnatitle']
        sbx_qnaContent = request.form['sbx_qnaContent']
        chk_QnaShow = request.form['chk_QnaShow']
        sessionId = request.form['sessionId']


        logging.debug("====Param data====")

        logging.debug("ipt_wrId = " + ipt_wrId)
        logging.debug("ipt_qnatitle = " + ipt_qnatitle)
        logging.debug("sbx_qnaContent = " + sbx_qnaContent)
        logging.debug("chk_QnaShow = " + chk_QnaShow)
        logging.debug("sessionId = " + sessionId)


        logging.debug("=====================")



        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)


        logging.debug("save Start")

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql= "INSERT INTO TB_QNA_TEST (QNA_NO, QNA_ORIGIN_NO, DATA_DEPTH, QNA_SORTS, QNA_WR_NM, " \
                                                "QNA_TITLE, " \
                                                "QNA_MAIN, " \
                                                "QNA_OPEN_YN, " \
                                                "QNA_RGS_DATE) " \
                     "VALUES(nextval(QNA_SEQ2), lastval(QNA_SEQ2), 0, 0 , '" + sessionId + "', " \
                                            "'" + ipt_qnatitle + "', " \
                                            "'" + sbx_qnaContent + "', " \
                                            "'" + chk_QnaShow + "', " \
                                            "DATE_ADD(NOW(), INTERVAL 9 HOUR))"


                logger.info(sql)
                cursor.execute(sql)
                mysql_con.commit()

        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been saved successfully"
        }

        return jsonify(retJson)

class questiondetail(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        logging.debug('================== App Start ==================')
        logging.debug(data)
        logging.debug(data["number"])
        logging.debug(request.args.get('number'))
        logging.debug(request.args.get('param'))
        logging.debug('================== App End ==================')

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                if data["status"] == "R":
                    sql1 = "UPDATE TB_QNA_TEST SET QNA_CNT = QNA_CNT+1 WHERE QNA_NO = '" + data["number"] + "'"

                    logging.debug(sql1)
                    cursor.execute(sql1)
                    mysql_con.commit()

                sql2 = "SELECT A.*, B.ORIGIN_WR " \
                        "FROM TB_QNA_TEST A, " \
                        "(SELECT QNA_WR_NM ORIGIN_WR FROM TB_QNA_TEST A WHERE QNA_NO  = (SELECT QNA_ORIGIN_NO FROM TB_QNA_TEST WHERE QNA_NO = '"+ data["number"] +"')) B " \
                        "WHERE QNA_NO ='"+ data["number"] +"'"


                logger.debug(sql2)
                cursor.execute(sql2)
                
                logging.debug('questionDtPop SUCCESS')

        finally:
            mysql_con.close()
            logging.debug('questionDtPop CLOSE')

        result1 = cursor.fetchall()

        return result1

class questionDel(Resource):
    def post(self):
        params = request.get_json()
        logger.info(params)

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        number = request.form['number']
        isOrigin = request.form['isOrigin']
        sessionId = request.form['sessionId']


        logging.debug("====Param data====")

        logging.debug("number = " + number)
        logging.debug("isOrigin = " + isOrigin)
        logging.debug("sessionId = " + sessionId)


        logging.debug("=====================")



        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)


        logging.debug("delete Start")

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                if isOrigin == "0":
                    sql = "UPDATE TB_QNA_TEST SET QNA_DEL_YN = 'Y' WHERE QNA_ORIGIN_NO = " + number
                else :
                    sql= "UPDATE TB_QNA_TEST SET QNA_DEL_YN = 'Y' WHERE QNA_NO = " + number

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


class questionAw(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        logging.debug('================== App Start ==================')
        logging.debug(data)
        logging.debug(data["number"])
        logging.debug(request.args.get(''))
        logging.debug(request.args.get('param'))
        logging.debug('================== App End ==================')

        #requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT * FROM TB_QNA_TEST WHERE QNA_NO ='"+ data["number"] +"'"

                logging.debug(sql)
                cursor.execute(sql)
                logging.debug('questionAw SUCCESS')

        finally:
            mysql_con.close()
            logging.debug('questionAw CLOSE')

        result1 = cursor.fetchall()

        return result1

class qnaAnserReg(Resource):
    def post(self):
        logger.info('========app.py qnaAnserReg=========')
        params = request.get_json()
        logger.info(params)

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        asWrID = request.form['asWrID']
        asTitle = request.form['asTitle']
        asContents = request.form['asContents']
        originNo = request.form['originNo']
        originDepth = request.form['originDepth']
        originSort = request.form['originSort']



        logging.debug("====Param data====")

        logging.debug("asWrID = " + asWrID)
        logging.debug("asTitle = " + asTitle)
        logging.debug("asContents = " + asContents)
        logging.debug("originNo = " + originNo)
        logging.debug("originDepth = " + originDepth)
        logging.debug("originSort = " + originSort)


        logging.debug("=====================")



        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)


        logging.debug("answer save Start")

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql1 = "UPDATE TB_QNA_TEST SET QNA_SORTS = QNA_SORTS + 1 " \
                       "WHERE QNA_ORIGIN_NO = " + originNo + " AND " \
                       "QNA_SORTS >= " + originSort

                logger.info(sql1)
                cursor.execute(sql1)

                sql2 = "INSERT INTO TB_QNA_TEST (QNA_NO, QNA_ORIGIN_NO, " \
                                               "DATA_DEPTH, " \
                                               "QNA_SORTS, " \
                                               "QNA_WR_NM, " \
                                                "QNA_TITLE, " \
                                                "QNA_MAIN, " \
                                                "QNA_RGS_DATE) " \
                     "VALUES(nextval(QNA_SEQ2), " + originNo + ", " + originDepth + ", " + originSort + ", " \
                                            "'" + asWrID +"', " \
                                            "'" + asTitle +"', " \
                                            "'" + asContents +"', " \
                                            "DATE_ADD(NOW(), INTERVAL 9 HOUR))"


                logger.info(sql2)
                cursor.execute(sql2)

                mysql_con.commit()

        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been saved successfully"
        }

        return jsonify(retJson)

class qnaUpdate(Resource):
    def post(self):
        params = request.get_json()
        logger.info(params)

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        asWrID = request.form['asWrID']
        asTitle = request.form['asTitle']
        asContents = request.form['asContents']
        number = request.form['number']


        logging.debug("====Param data====")

        logging.debug("asWrID = " + asWrID)
        logging.debug("asTitle = " + asTitle)
        logging.debug("asContents = " + asContents)
        logging.debug("number = " + number)

        logging.debug("=====================")



        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)


        logging.debug("qnaUpdate save Start")

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "UPDATE TB_QNA_TEST SET " \
                       "QNA_TITLE = '" + asTitle +"', " \
                       "QNA_MAIN = '" + asContents +"', " \
                       "QNA_REWR_NM = '" + asWrID + "', " \
                       "QNA_REWR_DATE = DATE_ADD(NOW(), INTERVAL 9 HOUR) " \
                       "WHERE QNA_NO = " + number

                logger.info(sql)
                cursor.execute(sql)

                mysql_con.commit()

        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been saved successfully"
        }

        return jsonify(retJson)

class qnaUpdateCnt(Resource):
    def post(self):
        params = request.get_json()
        logger.info(params)

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        number = request.form['number']
        
        logging.debug("====Param data====")

        logging.debug("number = " + number)

        logging.debug("=====================")



        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)


        logging.debug("count update Start")

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql= "UPDATE TB_QNA_TEST SET QNA_CNT = QNA_CNT+1 WHERE QNA_NO = " + number

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

class qnaSearch(Resource):  # Mariadb 연결 진행
    def get(self):
        logging.debug("qnaSearch app.py start")
        data =request.get_json()

        # get data
        option = data["option"]
        keyword = data["keyword"]


        logging.debug('================== App Start ==================')
        logging.debug(data)
        logging.debug(data["option"])
        logging.debug(data["keyword"])
        logging.debug('================== App End ==================')

        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT A.QNA_WR_NM ORIGIN_WR, B.*  FROM TB_QNA_TEST  A, TB_QNA_TEST B WHERE " \
                      "A.QNA_NO = B.QNA_ORIGIN_NO AND " \
                      "B.QNA_ORIGIN_NO NOT IN (SELECT QNA_NO FROM TB_QNA_TEST WHERE DATA_DEPTH = 0 AND QNA_DEL_YN = 'Y') AND " \
                      "B.QNA_ORIGIN_NO IN(SELECT QNA_NO FROM TB_QNA_TEST WHERE DATA_DEPTH = '0' AND "

                if option == "00" : #제목
                    sql += "QNA_TITLE LIKE '%"+ keyword +"%'"
                if option == "01" : #내용
                    sql += "QNA_MAIN LIKE '%"+ keyword +"%'"
                if option == "02" : #제목+내용
                    sql += "QNA_TITLE LIKE '%"+ keyword +"%' OR QNA_MAIN LIKE '%"+ keyword +"%'"
                if option == "03" : #작성자
                    sql += "QNA_WR_NM LIKE '%"+ keyword +"%'"

                sql += ")ORDER BY B.QNA_ORIGIN_NO DESC, B.QNA_SORTS ASC"

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

class updateRestTm(Resource):  # Mariadb 연결 진행
    def post(self):

        params = json.loads(request.data)
        logger.info("App Parameters Start")
        logger.info(params['email'])
        logger.info("App Parameters End")

        email = params['email']
        dt = params['dt']
        restTm = params['restTm']

        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "UPDATE TB_WRK_TM_MGMT_M " \
                      "   SET REST_TM  = %s " \
                      "   WHERE EMP_EMAL_ADDR = %s " \
                      "   AND WRK_DT = %s "
                logger.info(sql)
                cursor.execute(sql, (restTm, email, dt))
                mysql_con.commit()

        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been saved successfully"
        }

        return jsonify(retJson)
class updateDinnRestTm(Resource):  # Mariadb 연결 진행
    def post(self):

        params = json.loads(request.data)
        logger.info("App Parameters Start")
        logger.info(params['email'])
        logger.info("App Parameters End")

        email = params['email']
        dt = params['dt']
        dinnRestTm = params['dinnRestTm']

        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "UPDATE TB_WRK_TM_MGMT_M " \
                      "   SET DINN_REST_TM  = %s " \
                      "   WHERE EMP_EMAL_ADDR = %s " \
                      "   AND WRK_DT = %s "
                logger.info(sql)
                cursor.execute(sql, (dinnRestTm, email, dt))
                mysql_con.commit()

        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been saved successfully"
        }

        return jsonify(retJson)

    
api.add_resource(Hello, '/hello')
api.add_resource(Register, '/register')
api.add_resource(Retrieve, '/retrieve')
api.add_resource(Save, '/save')

api.add_resource(mariatestDB,'/mariatestDB') #api 선언
api.add_resource(wrkTimeInfoByEml,'/wrkTimeInfoByEml')      #_
api.add_resource(yryMgmt,'/yryMgmt')                        #_
api.add_resource(hldyMgmt,'/hldyMgmt')                      #_
api.add_resource(wrkApvlReq,'/wrkApvlReq')                  #_
api.add_resource(saveApvlReq,'/saveApvlReq')                #근무 결재 요청 저장
api.add_resource(saveApvlAcpt,'/saveApvlAcpt')              #근무 결재 승인 저장
api.add_resource(apvlReqHist,'/apvlReqHist')                #근무 결재 요청 내역 조회
api.add_resource(duplApvlReqCnt,'/duplApvlReqCnt')          #동일 일자 근무 결재 요청 내역 건수 조회
api.add_resource(apvlReqHistDetl,'/apvlReqHistDetl')        #근무 결재 요청 상세 조회
api.add_resource(apvlAcptHist,'/apvlAcptHist')              #근무 결재 승인 내역 조회
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
api.add_resource(empName,'/empName')                        #이메일로 사용자 이름 조회
api.add_resource(empDept,'/empDept')                        #이메일로 사용자 부서 정보 조회
api.add_resource(empDeptGm,'/empDeptGm')                      #이메일로 사용자 부서 사업부장(GM) 정보 조회
api.add_resource(empDeptPr,'/empDeptPr')                      #이메일로 사용자 부서 현장대리인(PR) 정보 조회
api.add_resource(saveYryApvlReq,'/saveYryApvlReq')          #_
api.add_resource(weekGridData,'/weekGridData') #api 선언
api.add_resource(apvlInfo,'/apvlInfo') #api 선언
api.add_resource(monthGridData,'/monthGridData') #api 선언
api.add_resource(insertStrtTm,'/insertStrtTm') #api 선언
api.add_resource(updateEndTm,'/updateEndTm') #api 선언
api.add_resource(yryUseDays,'/yryUseDays') #api 선언
api.add_resource(retrieveCmmCd,'/retrieveCmmCd')            #공통 코드 조회
api.add_resource(scheduleStatLst,'/scheduleStatLst') #api 선언
api.add_resource(totalWrktm,'/totalWrktm') #api 선언
api.add_resource(empMgmtRegSubmit,'/empMgmtRegSubmit') #api 선언
api.add_resource(isExistEmpNm,'/isExistEmpNm') #api 선언
api.add_resource(empOneInfo,'/empOneInfo') #api 선언
api.add_resource(empMgmtEditSubmit,'/empMgmtEditSubmit') #api 선언
api.add_resource(empMgmtDelSubmit,'/empMgmtDelSubmit') #api 선언
api.add_resource(question,'/question') #api 선언
api.add_resource(questionInfo,'/questionInfo') #api 선언
api.add_resource(qnaPopCnt,'/qnaPopCnt') #api 선언
api.add_resource(qnaPopUp,'/qnaPopUp') #api 선언
api.add_resource(questionWrSubmit,'/questionWrSubmit') #api 선언
api.add_resource(questiondetail,'/questiondetail') #api 선언
api.add_resource(questionDel,'/questionDel') #api선언
api.add_resource(questionAw,'/questionAw') #api선언
api.add_resource(qnaAnserReg,'/qnaAnserReg') #api선언
api.add_resource(qnaUpdate,'/qnaUpdate') #api선언
api.add_resource(qnaUpdateCnt,'/qnaUpdateCnt') #api선언
api.add_resource(qnaSearch,'/qnaSearch') #api선언
api.add_resource(updateRestTm,'/updateRestTm') #api선언
api.add_resource(updateDinnRestTm,'/updateDinnRestTm') #api선언

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5006, debug=True)