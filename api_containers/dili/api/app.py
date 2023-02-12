#-*-coding:utf-8-*-
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from datetime import date, timedelta        # 연차 등록 시, 근무시간 레코드 등록을 위한 날짜 리스트 추출 용도로  추가
#from pymongo import MongoClient
import logging
logging.basicConfig(level=logging.DEBUG)
import bcrypt
import socket

#from bson.json_util import dumps
import json
import pymysql
import os

app = Flask(__name__)
api = Api(app)
logger = logging.getLogger(__name__)
app.config['JSON_AS_ASCII'] = False

import datetime
from json import JSONEncoder

class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

def getMariaConn():
    logging.debug('====================='+os.environ['MYSQL_HOST'])

    logging.info(os.environ['MYSQL_HOST'])
    logging.info(os.environ['MYSQL_PORT'])
    logging.info(os.environ['MYSQL_DATABASE'])
    logging.info(os.environ['MYSQL_USER'])
    logging.info(os.environ['MYSQL_PASSWORD'])

    return pymysql.connect(
            host=getSystemInfo(),
            port=int(os.environ['MYSQL_PORT']),
            db=os.environ['MYSQL_DATABASE'],
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            charset='utf8')

def getSystemInfo():
    logging.debug('dill Server')
    logging.debug("=====>>>>>>>>>>> " + os.environ['SPRING_PROFILES_ACTIVE'])
    try:
        if (os.environ['SPRING_PROFILES_ACTIVE'] == "prod" ) :
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
        #mysql_con = pymysql.connect(host=getSystemInfo() , port=3306, db='IFG_IMS', user='ims2', password='1234',
        #                                charset='utf8', autocommit=False)
        mysql_con = getMariaConn()
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
        #mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
        #                                charset='utf8', autocommit=False)
        mysql_con = getMariaConn()

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
        #mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
        #                                charset='utf8', autocommit=False)
        mysql_con = getMariaConn()

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT (SELECT CONCAT(COUNT(*) * 8)"\
                      "          FROM TB_DATE"\
                      "         WHERE YMD_DATE LIKE '" + data["dt"] + "%'"\
                      "           AND HOLY_GB  = 'N') AS WRK_TOT_TM" \
                      "       ,(SELECT CONCAT(TRUNCATE((COUNT(*) / 7) * 12, 2))" \
                      "          FROM TB_DATE" \
                      "         WHERE YMD_DATE LIKE '" + data["dt"] + "%') AS EXTN_WRK_PSBL_TM"\
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
        #mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
        #                                charset='utf8', autocommit=False)
        mysql_con = getMariaConn()

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
        #mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
        #                                charset='utf8', autocommit=False)
        mysql_con = getMariaConn()

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql =  "WITH TMP_WRK AS (                                                                                                                            " \
                       +"				 SELECT *                                                                                                                    " \
                       +"				   FROM TB_WRK_TM_MGMT_M                                                                                                     " \
                       +"                  WHERE EMP_EMAL_ADDR = '" + data["email"] + "'                                                                              " \
                       +"                    AND WRK_DT >= '" + data["strtDt"] + "'                                                                                   " \
                       +"                    AND WRK_DT <= '" + data["endDt"] + "'                                                                                    " \
                       +"                 )                                                                                                                           " \
                       +"SELECT  '' AS WRK_SEQ                                                                                                                        " \
                       +"       ,A.EMP_EMAL_ADDR                                                                                                                      " \
                       +"       ,A.WRK_DT                                                                                                                             " \
                       +"       ,NVL(DATE_FORMAT(A.JOB_STRT_TM, '%H:%i'),'-') AS JOB_STRT_TM                                                                          " \
                       +"       ,NVL(DATE_FORMAT(A.JOB_END_TM, '%H:%i'),'-') AS JOB_END_TM                                                                            " \
                       +"       ,CONCAT(LPAD(SUBSTRING(LPAD(A.JOB_END_TM - A.JOB_STRT_TM,6,'0'),1,2)-A.REST_TM/60,2,0),':',SUBSTRING(LPAD(A.JOB_END_TM - A.JOB_STRT_TM,6,'0'),3,2)) AS WRK_TM" \
                       +"	   ,A.REST_TM AS REST_TM                                                                                                                 " \
                       +"	   ,'' AS APVL_REQ_DIVS                                                                                                                  " \
                       +"       ,'' AS APVL_REQ_DIVS_NM                                                                                                               " \
                       +"       ,'' AS HOLI_TERM1                                                                                                                     " \
                       +"       ,'' AS HOLI_TERM2                                                                                                                     " \
                       +"       ,'' AS PTO_KD_CD                                                                                                                      " \
                       +"	   ,'' AS PTO_KD_CD_NM                                                                                                                    " \
                       +"       ,'' AS HDO_KD_CD                                                                                                                      " \
                       +"       ,'' AS HDO_KD_CD_NM                                                                                                                   " \
                       +"       ,'' AS APVL_STTS_CD_NM                                                                                                                " \
                       +"  FROM TMP_WRK A                                                                                                                             " \
                       +" WHERE 1 = 1                                                                                                                                 " \
                       +"   AND WRK_DT NOT IN (                                                                                                                       " \
                       +"	      			  SELECT   A.WRK_DT                                                                                                        " \
                       +"                        FROM TMP_WRK A                                                                                                       " \
                       +"						JOIN TB_NEW_APVL_REQ_MGMT_M B                                                                                          " \
                       +"				          ON (A.WRK_DT = B.WRK_DT OR A.WRK_DT  BETWEEN B.HOLI_TERM1 AND B.HOLI_TERM2)                                          " \
                       +"                       WHERE 1 = 1                                                                                                           " \
                       +"					     AND A.EMP_EMAL_ADDR = B.EMP_EMAL_ADDR                                                                                 " \
                       +"                         AND B.APVL_REQ_DIVS = '03'                                                                                          " \
                       +"			         )                                                                                                                         " \
                       +"				                                                                                                                               " \
                       +"UNION ALL                                                                                                                                    " \
                       +"                                                                                                                                             " \
                       +"SELECT B.WRK_SEQ AS WRK_SEQ                                                                                                                  " \
                       +"      ,B.EMP_EMAL_ADDR                                                                                                                       " \
                       +"      ,B.WRK_DT                                                                                                                              " \
                       +"      ,NVL(DATE_FORMAT(B.JOB_STRT_TM, '%H:%i'),'-') AS JOB_STRT_TM                                                                           " \
                       +"      ,NVL(DATE_FORMAT(B.JOB_END_TM, '%H:%i'),'-') AS JOB_END_TM                                                                             " \
                       +"	  ,(CASE WHEN B.PTO_KD_CD = '01'                                                                                                         " \
                       +"             THEN '08:00'                                                                                                                    " \
                       +"             WHEN B.PTO_KD_CD = '02'                                                                                                         " \
                       +"             THEN '4:00'                                                                                                                     " \
                       +"             ELSE IF (                                                                                                                       " \
                       +"                          SUBSTRING(LPAD(B.JOB_END_TM - B.JOB_STRT_TM,6,'0'),3,2) < B.REST_TM % 60                                           " \
                       +"                         , CONCAT(SUBSTRING(LPAD(B.JOB_END_TM - B.JOB_STRT_TM,6,'0'),1,2)-1,':',60 - B.REST_TM % 60)                         " \
                       +"                         ,CONCAT(SUBSTRING(LPAD(B.JOB_END_TM - B.JOB_STRT_TM,6,'0'),1,2),':',IF( SUBSTRING(LPAD(B.JOB_END_TM - B.JOB_STRT_TM,6,'0'),3,2) > 60,SUBSTRING(LPAD(B.JOB_END_TM - B.JOB_STRT_TM,6,'0'),3,2)-40,SUBSTRING(LPAD(B.JOB_END_TM - B.JOB_STRT_TM,6,'0'),3,2) ) - B.REST_TM % 60) " \
                       +"                       )                                                                                                                     " \
                       +"              END                                                                                                                            " \
                       +"        ) AS WRK_TM                                                                                                                          " \
                       +"	   ,NVL(B.REST_TM,0) AS REST_TM                                                                                                           " \
                       +"      ,B.APVL_REQ_DIVS AS APVL_REQ_DIVS                                                                                                      " \
                       +"      ,NVL((SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL WHERE CMM_CD_GRP_ID = 'APVL_DIVS_CD' AND CMM_CD = B.APVL_REQ_DIVS),'') AS APVL_REQ_DIVS_NM" \
                       +"      ,NVL(B.HOLI_TERM1,'') AS HOLI_TERM1                                                                                                    " \
                       +"      ,NVL(B.HOLI_TERM2,'') AS HOLI_TERM2                                                                                                    " \
                       +"      ,NVL(B.PTO_KD_CD,'') AS PTO_KD_CD                                                                                                      " \
                       +"      ,NVL((SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL WHERE CMM_CD_GRP_ID = 'PTO_KD_CD' AND CMM_CD = B.PTO_KD_CD),'') AS PTO_KD_CD_NM           " \
                       +"      ,NVL(B.HDO_KD_CD,'') AS HDO_KD_CD                                                                                                      " \
                       +"      ,NVL((SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL WHERE CMM_CD_GRP_ID = 'HDO_KD_CD' AND CMM_CD = B.HDO_KD_CD),'') AS HDO_KD_CD_NM           " \
                       +"      ,(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL                                                                                               " \
                       +"         WHERE CMM_CD_GRP_ID = 'APVL_STTS_CD'                                                                                                " \
                       +"           AND CMM_CD = ((CASE WHEN B.TH1_APRV_STUS = '01'                                                                                   " \
                       +"                              THEN '01'                                                                                                      " \
                       +"                              WHEN B.TH2_APRV_STUS = '02'                                                                                    " \
                       +"                              THEN '03'                                                                                                      " \
                       +"                              WHEN B.TH1_APRV_STUS = '02'                                                                                    " \
                       +"                              THEN '02'                                                                                                      " \
                       +"                              WHEN B.TH1_APRV_STUS = '03'                                                                                    " \
                       +"                              THEN '04'                                                                                                      " \
                       +"                               END  ))                                                                                                       " \
                       +"       ) AS APVL_STTS_CD_NM                                                                                                                  " \
                       +" FROM TB_WRK_TM_MGMT_M A                                                                                                                     " \
                       +" RIGHT JOIN TB_NEW_APVL_REQ_MGMT_M B                                                                                                         " \
                       +"   ON (A.EMP_EMAL_ADDR = B.EMP_EMAL_ADDR AND (B.WRK_DT = A.WRK_DT OR A.WRK_DT  BETWEEN B.HOLI_TERM1 AND B.HOLI_TERM2 ))                      " \
                       +"WHERE B.EMP_EMAL_ADDR = '" + data["email"] + "'                                                                                              " \
                       +"  AND B.WRK_DT >= '" + data["strtDt"] + "'                                                                                                   " \
                       +"  AND B.WRK_DT <= '" + data["endDt"] + "'                                                                                                    " \
                       +"ORDER BY WRK_DT, JOB_STRT_TM                                                                                                                 "


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
        #mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
        #                                charset='utf8', autocommit=False)
        mysql_con = getMariaConn()

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT  NVL(APVL_REQ_DT, 'N/A') AS APVL_REQ_DT "\
                    + "       ,NVL(APVL_LAST_APRV_DT, 'N/A') AS APVL_LAST_APRV_DT "\
                    + "       ,NVL(TH1_APRV_STUS, 'N/A') AS TH1_APRV_STUS "\
                    + "       ,NVL(TH2_APRV_STUS, 'N/A') AS TH2_APRV_STUS "\
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
        #mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
        #                                charset='utf8', autocommit=False)
        mysql_con = getMariaConn()

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                logger.debug('========= sql generat')
                #쿼리문 실행
                sql =  "WITH TMP_WRK AS (                                                                                                                            " \
                       +"				 SELECT *                                                                                                                    " \
                       +"				   FROM TB_WRK_TM_MGMT_M                                                                                                     " \
                       +"                 WHERE EMP_EMAL_ADDR = '" + data["email"] + "'                                                                            " \
                       +"                   AND WRK_DT like '"+data["mDt"]+"%'                                                                                     " \
                       +"                 )                                                                                                                           " \
                       +"SELECT  '' AS WRK_SEQ                                                                                                                        " \
                       +"       ,A.EMP_EMAL_ADDR                                                                                                                      " \
                       +"       ,A.WRK_DT                                                                                                                             " \
                       +"       ,NVL(DATE_FORMAT(A.JOB_STRT_TM, '%H:%i'),'-') AS JOB_STRT_TM                                                                          " \
                       +"       ,NVL(DATE_FORMAT(A.JOB_END_TM, '%H:%i'),'-') AS JOB_END_TM                                                                            " \
                       +"       ,CONCAT(LPAD(SUBSTRING(LPAD(A.JOB_END_TM - A.JOB_STRT_TM,6,'0'),1,2)-A.REST_TM/60,2,0),':',SUBSTRING(LPAD(A.JOB_END_TM - A.JOB_STRT_TM,6,'0'),3,2)) AS WRK_TM" \
                       +"	   ,A.REST_TM AS REST_TM                                                                                                                 " \
                       +"	   ,'' AS APVL_REQ_DIVS                                                                                                                  " \
                       +"       ,'' AS APVL_REQ_DIVS_NM                                                                                                               " \
                       +"       ,'' AS HOLI_TERM1                                                                                                                     " \
                       +"       ,'' AS HOLI_TERM2                                                                                                                     " \
                       +"       ,'' AS PTO_KD_CD                                                                                                                      " \
                       +"	    ,'' AS PTO_KD_CD_NM                                                                                                                   " \
                       +"       ,'' AS HDO_KD_CD                                                                                                                      " \
                       +"       ,'' AS HDO_KD_CD_NM                                                                                                                   " \
                       +"       ,'' AS APVL_STTS_CD_NM                                                                                                                " \
                       +"  FROM TMP_WRK A                                                                                                                             " \
                       +" WHERE 1 = 1                                                                                                                                 " \
                       +"   AND WRK_DT NOT IN (                                                                                                                       " \
                       +"	      			  SELECT   A.WRK_DT                                                                                                       " \
                       +"                        FROM TMP_WRK A                                                                                                       " \
                       +"						JOIN TB_NEW_APVL_REQ_MGMT_M B                                                                                         " \
                       +"				          ON (A.WRK_DT = B.WRK_DT OR A.WRK_DT  BETWEEN B.HOLI_TERM1 AND B.HOLI_TERM2)                                         " \
                       +"                       WHERE 1 = 1                                                                                                           " \
                       +"					     AND A.EMP_EMAL_ADDR = B.EMP_EMAL_ADDR                                                                                " \
                       +"                         AND B.APVL_REQ_DIVS = '03'                                                                                          " \
                       +"			         )                                                                                                                        " \
                       +"				                                                                                                                              " \
                       +"UNION ALL                                                                                                                                    " \
                       +"                                                                                                                                             " \
                       +"SELECT B.WRK_SEQ AS WRK_SEQ                                                                                                                  " \
                       +"      ,A.EMP_EMAL_ADDR                                                                                                                       " \
                       +"      ,A.WRK_DT                                                                                                                              " \
                       +"      ,NVL(DATE_FORMAT(B.JOB_STRT_TM, '%H:%i'),'-') AS JOB_STRT_TM                                                                           " \
                       +"      ,NVL(DATE_FORMAT(B.JOB_END_TM, '%H:%i'),'-') AS JOB_END_TM                                                                             " \
                       +"	  ,(CASE WHEN B.PTO_KD_CD = '01'                                                                                                          " \
                       +"             THEN '08:00'                                                                                                                    " \
                       +"             WHEN B.PTO_KD_CD = '02'                                                                                                         " \
                       +"             THEN '4:00'                                                                                                                     " \
                       +"             ELSE CONCAT(SUBSTRING(LPAD(B.JOB_END_TM - B.JOB_STRT_TM,6,'0'),1,2),':',SUBSTRING(LPAD(B.JOB_END_TM - B.JOB_STRT_TM,6,'0'),3,2))" \
                       +"              END                                                                                                                            " \
                       +"        ) AS WRK_TM                                                                                                                          " \
                       +"	   ,NVL(B.REST_TM,0) AS REST_TM                                                                                                           " \
                       +"      ,B.APVL_REQ_DIVS AS APVL_REQ_DIVS                                                                                                      " \
                       +"      ,NVL((SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL WHERE CMM_CD_GRP_ID = 'APVL_DIVS_CD' AND CMM_CD = B.APVL_REQ_DIVS),'') AS APVL_REQ_DIVS_NM" \
                       +"      ,NVL(B.HOLI_TERM1,'') AS HOLI_TERM1                                                                                                    " \
                       +"      ,NVL(B.HOLI_TERM2,'') AS HOLI_TERM2                                                                                                    " \
                       +"      ,NVL(B.PTO_KD_CD,'') AS PTO_KD_CD                                                                                                      " \
                       +"      ,NVL((SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL WHERE CMM_CD_GRP_ID = 'PTO_KD_CD' AND CMM_CD = B.PTO_KD_CD),'') AS PTO_KD_CD_NM           " \
                       +"      ,NVL(B.HDO_KD_CD,'') AS HDO_KD_CD                                                                                                      " \
                       +"      ,NVL((SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL WHERE CMM_CD_GRP_ID = 'HDO_KD_CD' AND CMM_CD = B.HDO_KD_CD),'') AS HDO_KD_CD_NM           " \
                       +"      ,(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL                                                                                               " \
                       +"         WHERE CMM_CD_GRP_ID = 'APVL_STTS_CD'                                                                                                " \
                       +"           AND CMM_CD = ((CASE WHEN B.TH1_APRV_STUS = '01'                                                                                   " \
                       +"                              THEN '01'                                                                                                      " \
                       +"                              WHEN B.TH2_APRV_STUS = '02'                                                                                    " \
                       +"                              THEN '03'                                                                                                      " \
                       +"                              WHEN B.TH1_APRV_STUS = '02'                                                                                    " \
                       +"                              THEN '02'                                                                                                      " \
                       +"                              WHEN B.TH1_APRV_STUS = '03'                                                                                    " \
                       +"                              THEN '04'                                                                                                      " \
                       +"                               END  ))                                                                                                       " \
                       +"       ) AS APVL_STTS_CD_NM                                                                                                                  " \
                       +" FROM TMP_WRK A                                                                                                                              " \
                       +" JOIN TB_NEW_APVL_REQ_MGMT_M B                                                                                                               " \
                       +"   ON (A.WRK_DT = B.WRK_DT OR A.WRK_DT  BETWEEN B.HOLI_TERM1 AND B.HOLI_TERM2)                                                               " \
                       +"WHERE A.EMP_EMAL_ADDR = B.EMP_EMAL_ADDR                                                                                                      " \
                       +"  AND B.APVL_REQ_DIVS <> '99'                                                                                                                " \
                       +"ORDER BY WRK_DT, JOB_STRT_TM                                                                                                                 "

                logger.debug('========= sql generated')
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
        #mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
        #                                charset='utf8', autocommit=False)
        mysql_con = getMariaConn()

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT A.EMP_EMAL_ADDR" \
                    + "      ,DATE_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.NORM_WRK_TM,1,2),':',SUBSTRING(A.NORM_WRK_TM,3,2),':',SUBSTRING(A.NORM_WRK_TM,5,2)) ,'%H:%i:%S')))),'%H.%i') NORM_WRK_TM" \
                    + "      ,DATE_FORMAT(SEC_TO_TIME((SUM(TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.HLDY_WRK_TM,1,2),':',SUBSTRING(A.HLDY_WRK_TM,3,2),':',SUBSTRING(A.HLDY_WRK_TM,5,2)) ,'%H:%i:%S'))) + SUM(TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(A.NGHT_WRK_TM,1,2),':',SUBSTRING(A.NGHT_WRK_TM,3,2),':',SUBSTRING(A.NGHT_WRK_TM,5,2)) ,'%H:%i:%S')))) - SUM(TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(IFNULL(B.WRK_TME,'000000'),1,2),':',SUBSTRING(IFNULL(B.WRK_TME,'000000'),3,2),':',SUBSTRING(IFNULL(B.WRK_TME,'000000'),5,2)) ,'%H:%i:%S')))),'%H.%i') NOT_APRV_OVER_WRK_TM" \
                    + "      ,DATE_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(STR_TO_DATE( CONCAT(SUBSTRING(IFNULL(B.WRK_TME,'000000'),1,2),':',SUBSTRING(IFNULL(B.WRK_TME,'000000'),3,2),':',SUBSTRING(IFNULL(B.WRK_TME,'000000'),5,2)) ,'%H:%i:%S')))),'%H.%i') APRV_OVER_WRK_TM" \
                    + "      ,MAX(DATE_FORMAT(E.JOB_STRT_TM, '%H:%i')) AS JOB_STRT_TM " \
                    + "      ,MAX(DATE_FORMAT(E.JOB_END_TM, '%H:%i')) AS JOB_END_TM " \
                    + "  FROM TB_WRK_TM_MGMT_M A INNER JOIN TB_EMP_MGMT E ON A.EMP_EMAL_ADDR = E.EMP_EMAIL LEFT OUTER JOIN TB_APVL_REQ_MGMT_M B ON A.EMP_EMAL_ADDR = B.EMP_EMAL_ADDR AND A.WRK_DT = B.WRK_DT AND B.APVL_REQ_DIVS IN ('01','02')" \
                    + " WHERE A.EMP_EMAL_ADDR = '" +data["email"] + "'" \
                    + "   AND A.WRK_DT LIKE '" + data["dt"] + "%'" \
                    + " GROUP BY A.EMP_EMAL_ADDR"
                logging.debug(sql + "#####")
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('======wrkTimeInfoByEml row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)

class wrkApvlReq(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        #requirements pymysql import 후 커넥트 사용
        #mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
        #                                charset='utf8', autocommit=False)
        mysql_con = getMariaConn()

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
                      "            WHEN NVL(A.HLDY_WRK_TM,'') = 000000 AND NVL(A.NGHT_WRK_TM,'') != 000000 THEN '연장근무' " \
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


        currReqPopStts  = request.form['currReqPopStts']
        email           = request.form['email']
        apvlDivs        = request.form['apvlDivs']
        apvlReqDivs     = request.form['apvlReqDivs']
        wrkDt           = request.form['wrkDt']
        wrkSeq          = request.form['wrkSeq']
        jobStrtTm       = request.form['jobStrtTm']
        jobEndTm        = request.form['jobEndTm']
        wrkTme          = request.form['wrkTme']
        wrkReqRsn       = request.form['wrkReqRsn']
        th1AprvStus     = request.form['th1AprvStus']
        th1AprvNm       = request.form['th1AprvNm']
        th2AprvStus     = request.form['th2AprvStus']
        th2AprvNm       = request.form['th2AprvNm']
        refNm           = request.form['refNm']
        ref2Nm          = request.form['ref2Nm']
        restTm          = request.form['restTm']

        #requirements pymysql import 후 커넥트 사용
        #mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
        #                                charset='utf8', autocommit=False)
        mysql_con = getMariaConn()

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                if currReqPopStts == "register":
                    sql = "INSERT INTO TB_NEW_APVL_REQ_MGMT_M (" \
                                                          "`EMP_EMAL_ADDR`," \
                                                          "`APVL_REQ_DIVS`," \
                                                          "`WRK_DT`," \
                                                          "`WRK_SEQ`," \
                                                          "`JOB_STRT_TM`," \
                                                          "`JOB_END_TM`," \
                                                          "`WRK_TME`," \
                                                          "`WRK_REQ_RSN`," \
                                                          "`APVL_REQ_DT`," \
                                                          "`TH1_APRV_STUS`," \
                                                          "`TH1_APRV_NM`," \
                                                          "`TH2_APRV_STUS`," \
                                                          "`TH2_APRV_NM`," \
                                                          "`REF_NM`," \
                                                          "`REF2_NM`," \
                                                          "`REST_TM`," \
                                                          "`APVL_LAST_APRV_DT`)" \
                                                " VALUES (   '" + email       + "'"\
                                                          ", '" + apvlReqDivs + "'"\
                                                          ", '" + wrkDt       + "'"\
                                                          ", (SELECT NVL(MAX(WRK_SEQ), 0)+1" \
                                                          "     FROM TB_NEW_APVL_REQ_MGMT_M as WRKSEQ" \
                                                          "    WHERE EMP_EMAL_ADDR = '" + email + "'" \
                                                          "      AND WRK_DT = '" + wrkDt + "'" \
                                                          "  ) "\
                                                          ", '" + jobStrtTm   + "'"\
                                                          ", '" + jobEndTm    + "'"\
                                                          ", '" + wrkTme      + "'"\
                                                          ", '" + wrkReqRsn   + "'"\
                                                          ",      NOW()" \
                                                          ", '" + th1AprvStus + "'"\
                                                          ", '" + th1AprvNm   + "'"\
                                                          ", '" + th2AprvStus + "'"\
                                                          ", '" + th2AprvNm   + "'"\
                                                          ", '" + refNm       + "'"\
                                                          ", '" + ref2Nm      + "'"\
                                                          ", '" + restTm      + "'"\
                                                          ",      NOW()) ON DUPLICATE KEY " \
                          "UPDATE JOB_STRT_TM   = '"  + jobStrtTm   + "' " \
                          "     , JOB_END_TM    = '"  + jobEndTm    + "' " \
                          "     , WRK_TME       = '"  + wrkTme      + "' " \
                          "     , WRK_REQ_RSN   = '"  + wrkReqRsn   + "' " \
                          "     , TH1_APRV_NM   = '"  + th1AprvNm   + "' " \
                          "     , TH1_APRV_STUS = '"  + th1AprvStus + "' " \
                          "     , TH2_APRV_NM   = '"  + th2AprvNm   + "' " \
                          "     , TH2_APRV_STUS = '"  + th2AprvStus + "' " \
                          "     , REF_NM        = '"  + refNm       + "' " \
                          "     , REF2_NM       = '"  + ref2Nm      + "' " \
                          "     , REST_TM       = '"  + restTm      + "' " \
                          "     , APVL_REQ_DIVS = '"  + apvlReqDivs + "' " \
                          "     , APVL_UPD_DT   =       NOW() "
                if currReqPopStts == "modify":
                    sql = "UPDATE TB_NEW_APVL_REQ_MGMT_M " \
                          "   SET JOB_STRT_TM   = '"  + jobStrtTm   + "' " \
                          "     , JOB_END_TM    = '"  + jobEndTm    + "' " \
                          "     , WRK_TME       = '"  + wrkTme      + "' " \
                          "     , WRK_REQ_RSN   = '"  + wrkReqRsn   + "' " \
                          "     , TH1_APRV_NM   = '"  + th1AprvNm   + "' " \
                          "     , TH1_APRV_STUS = '"  + th1AprvStus + "' " \
                          "     , TH2_APRV_NM   = '"  + th2AprvNm   + "' " \
                          "     , TH2_APRV_STUS = '"  + th2AprvStus + "' " \
                          "     , REF_NM        = '"  + refNm       + "' " \
                          "     , REF2_NM       = '"  + ref2Nm      + "' " \
                          "     , REST_TM       = '"  + restTm      + "' " \
                          "     , APVL_UPD_DT   =       NOW() " \
                          " WHERE EMP_EMAL_ADDR = '"  + email       + "' " \
                          "   AND WRK_DT        = '"  + wrkDt       + "' " \
                          "   AND WRK_SEQ       = '"  + wrkSeq       + "' "

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
        th2AprvStus = request.form['th2AprvStus']
        authFlag = request.form['authFlag']

        #requirements pymysql import 후 커넥트 사용
        #mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
        #                                charset='utf8', autocommit=False)
        mysql_con = getMariaConn()

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                if authFlag == "1":
                    #쿼리문 실행
                    sql = " UPDATE TB_APVL_REQ_MGMT_M /*1차승인*/ " \
                          "    SET TH1_APRV_STUS     = '" + th1AprvStus + "'" \
                          "      , TH1_APRV_RSN      = '" + th1AprvRsn + "'" \
                          "      , TH1_APRV_DT       = NOW() " \
                          "      , APVL_LAST_APRV_DT = NOW() " \
                          "  WHERE EMP_EMAL_ADDR     = '" + email + "' " \
                          "    AND WRK_DT            = '" + wrkDt + "' " \
                          "    AND JOB_STRT_TM       = '" + jobStrtTm + "' " \
                          "    AND JOB_END_TM        = '" + jobEndTm + "' "

                elif authFlag == "2":
                    #쿼리문 실행
                    sql = " UPDATE TB_APVL_REQ_MGMT_M /*2차승인*/ " \
                          "    SET TH2_APRV_STUS     = '" + th2AprvStus + "'" \
                          "      , TH2_APRV_RSN      = '" + th1AprvRsn + "'" \
                          "      , TH2_APRV_DT       = NOW() " \
                          "      , APVL_LAST_APRV_DT = NOW() " \
                          "  WHERE EMP_EMAL_ADDR     = '" + email + "' " \
                          "    AND WRK_DT            = '" + wrkDt + "' " \
                          "    AND JOB_STRT_TM       = '" + jobStrtTm + "' " \
                          "    AND JOB_END_TM        = '" + jobEndTm + "' "
                elif authFlag == "3":
                    #쿼리문 실행
                    sql = " UPDATE TB_APVL_REQ_MGMT_M /*1차승인*/ " \
                          "    SET TH1_APRV_STUS     = '" + th1AprvStus + "'" \
                          "      , TH2_APRV_STUS     = '" + th1AprvStus + "'"\
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
        #mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
        #                                charset='utf8', autocommit=False)
        mysql_con = getMariaConn()

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT A.WRK_SEQ" \
                      "     , B.EMP_NAME " \
                      "     , A.EMP_EMAL_ADDR " \
                      "     , A.TH1_APRV_NM " \
                      "     , NVL(A.WRK_DT,'') WRK_DT " \
                      "     , NVL(A.JOB_STRT_TM, '') JOB_STRT_TM " \
                      "     , NVL(A.JOB_END_TM, '') JOB_END_TM " \
                      "     , CASE WHEN A.APVL_REQ_DIVS = '01' THEN NVL(A.WRK_TME,'') " \
                      "            WHEN A.APVL_REQ_DIVS = '02' THEN NVL(A.WRK_TME,'') " \
                      "            ELSE '' END WRK_TME  " \
                      "     , CASE WHEN A.APVL_REQ_DIVS = '01' THEN '연장근무' " \
                      "            WHEN A.APVL_REQ_DIVS = '02' THEN '휴일근무' " \
                      "            WHEN A.APVL_REQ_DIVS = '03' THEN '연차결재'  " \
                      "            WHEN A.APVL_REQ_DIVS = '04' THEN '반차결재'  " \
                      "            ELSE '' END APVL_REQ_NM  " \
                      "     , CASE WHEN A.TH1_APRV_STUS = '01' AND NVL(A.TH2_APRV_STUS, '01') = '01' THEN '미승인'" \
                      "            WHEN A.TH1_APRV_STUS = '02' AND NVL(A.TH2_APRV_STUS, '01') = '01' THEN '1차승인'" \
                      "            WHEN A.TH1_APRV_STUS = '02' AND NVL(A.TH2_APRV_STUS, '01') = '02' THEN '2차승인'" \
                      "            WHEN A.TH1_APRV_STUS = '03'  OR NVL(A.TH2_APRV_STUS, '01') = '03' THEN '반려'" \
                      "            ELSE '확인필요' END APRV_STUS_NM" \
                      "     , NVL(A.TH1_APRV_STUS, '') AS TH1_APRV_STUS" \
                      "     , NVL(A.TH2_APRV_STUS, '') AS TH2_APRV_STUS" \
                      "     , CASE WHEN A.TH1_APRV_STUS = '01' AND NVL(A.TH2_APRV_STUS, '01') = '01' THEN C.EMP_NAME" \
                      "            WHEN A.TH1_APRV_STUS = '02' AND NVL(A.TH2_APRV_STUS, '01') = '01' THEN C.EMP_NAME" \
                      "            WHEN A.TH1_APRV_STUS = '02' AND NVL(A.TH2_APRV_STUS, '02') = '02' THEN D.EMP_NAME" \
                      "            WHEN A.TH1_APRV_STUS = '03' AND A.TH2_APRV_STUS = '03' THEN C.EMP_NAME" \
                      "            WHEN A.TH2_APRV_STUS = '03' THEN D.EMP_NAME" \
                      "            ELSE '반려' END REF_NM" \
                      "     , IFNULL(A.APVL_REQ_DT, '') AS APVL_REQ_DT" \
                      "     , CONCAT(IFNULL(A.WRK_REQ_RSN, ''), IFNULL(A.HOLI_REQ_RSN, '')) AS WRK_REQ_RSN" \
                      "     , CASE WHEN A.APVL_REQ_DIVS = '03'" \
                      "            THEN IFNULL(CONCAT(A.HOLI_TERM1, ' ~ ', A.HOLI_TERM2), '') " \
                      "            ELSE ''" \
                      "        END AS YEONCHA" \
                      "     , CASE WHEN A.APVL_REQ_DIVS = '04'" \
                      "            THEN CONCAT(IFNULL(A.HOLI_TERM2, ''), '(', CASE WHEN A.HDO_KD_CD = '01' THEN '오전' ELSE '오후' END, ')') " \
                      "            ELSE ''" \
                      "        END AS BANCHA" \
                      "     , NVL(A.TH1_APRV_NM, '') AS TH1_APRV_NM " \
                      "     , NVL(A.TH2_APRV_NM, '') AS TH2_APRV_NM " \
                      "  FROM TB_NEW_APVL_REQ_MGMT_M A " \
                      "      ,TB_EMP_MGMT B" \
                      "      ,TB_EMP_MGMT C" \
                      "      ,TB_EMP_MGMT D" \
                      " WHERE A.EMP_EMAL_ADDR = B.EMP_EMAIL" \
                      "   AND A.TH1_APRV_NM = C.EMP_EMAIL " \
                      "   AND A.TH2_APRV_NM = D.EMP_EMAIL " \
                      "   AND A.APVL_REQ_DIVS <> '99'" \
                      "   AND A.APVL_REQ_DT LIKE '" + apvlReqDtYm + "%' "
                if apvlStusDivs == "01": #미승인
                    sql += "   AND A.TH1_APRV_STUS = '" + apvlStusDivs + "'"
                elif apvlStusDivs == "02" or apvlStusDivs == "03": #승인, 반려
                    sql += "   AND (A.TH1_APRV_STUS = '" + apvlStusDivs + "' OR A.TH2_APRV_STUS = '" + apvlStusDivs + "') "
                if email != "":
                    sql += "   AND A.EMP_EMAL_ADDR = '" + email + "' "
                if deptCd != "" and deptCd != "00":
                    sql += "   AND B.DEPT_CD = '" + deptCd + "' "

                sql += " ORDER BY A.APVL_REQ_DT ASC, A.WRK_DT ASC "
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
        empPr = data["empPr"]
        empGm = data["empGm"]
        apvlStusDivs = data["apvlStusDivs"]

        logging.debug('--------------- app.py apvlAcptHist data ---------------')
        logging.debug('email : '        + email)
        logging.debug('empPr : ' + empPr)
        logging.debug('empGm : ' + empGm)
        logging.debug('apvlStusDivs : ' + apvlStusDivs)
        logging.debug('------------------------------------')

        # requirements pymysql import 후 커넥트 사용
        #mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
        #                            charset='utf8', autocommit=False)
        mysql_con = getMariaConn()

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                if apvlStusDivs == "00":
                    # 전체
                    sql = "SELECT A.EMP_EMAL_ADDR, C.EMP_NAME " \
                          "     , NVL(A.WRK_DT,'') WRK_DT " \
                          "     , A.WRK_SEQ " \
                          "     , NVL(A.JOB_STRT_TM, '') JOB_STRT_TM " \
                          "     , NVL(A.JOB_END_TM, '') JOB_END_TM " \
                          "     , CASE WHEN A.APVL_REQ_DIVS = '01' THEN NVL(A.WRK_TME,'') WHEN A.APVL_REQ_DIVS = '02' THEN NVL(A.WRK_TME,'') ELSE '' END WRK_TME  " \
                          "     , CASE WHEN A.APVL_REQ_DIVS = '01' THEN '연장근무' WHEN A.APVL_REQ_DIVS = '02' THEN '휴일근무' WHEN A.APVL_REQ_DIVS = '03' THEN '연차결재' WHEN A.APVL_REQ_DIVS = '04' THEN '반차결재' ELSE '' END APVL_REQ_NM  " \
                          "     , CASE WHEN A.TH1_APRV_STUS = '01' AND NVL(A.TH2_APRV_STUS, '01') = '01' THEN '미승인'" \
                          "            WHEN A.TH1_APRV_STUS = '02' AND NVL(A.TH2_APRV_STUS, '01') = '01' THEN '1차승인'" \
                          "            WHEN A.TH1_APRV_STUS = '02' AND NVL(A.TH2_APRV_STUS, '01') = '02' THEN '2차승인'" \
                          "            WHEN A.TH1_APRV_STUS = '03'  OR NVL(A.TH2_APRV_STUS, '01') = '03' THEN '반려'" \
                          "            ELSE '확인필요' END APRV_STUS_NM" \
                          "     , NVL(A.APVL_REQ_DT, '') APVL_REQ_DT " \
                          "     , CONCAT(NVL(A.WRK_REQ_RSN, ''), NVL(A.HOLI_REQ_RSN, ''))  WRK_REQ_RSN " \
                          "     , NVL(A.TH1_APRV_STUS, '') AS TH1_APRV_STUS" \
                          "     , NVL(A.TH2_APRV_STUS, '') AS TH2_APRV_STUS" \
                          "     , CASE WHEN A.APVL_REQ_DIVS = '03'" \
                          "            THEN IFNULL(CONCAT(A.HOLI_TERM1, ' ~ ', A.HOLI_TERM2), '') " \
                          "            ELSE ''" \
                          "        END AS YEONCHA" \
                          "     , CASE WHEN A.APVL_REQ_DIVS = '04'" \
                          "            THEN CONCAT(IFNULL(A.HOLI_TERM2, ''), '(', CASE WHEN A.HDO_KD_CD = '01' THEN '오전' ELSE '오후' END, ')')  " \
                          "            ELSE ''" \
                          "        END AS BANCHA" \
                          "     , NVL(A.TH1_APRV_NM, '') AS TH1_APRV_NM " \
                          "     , NVL(A.TH2_APRV_NM, '') AS TH2_APRV_NM " \
                          "  FROM TB_NEW_APVL_REQ_MGMT_M A, TB_EMP_MGMT B, TB_EMP_MGMT C " \
                          " WHERE A.EMP_EMAL_ADDR = C.EMP_EMAIL  " \
                          "   AND A.TH1_APRV_NM = B.EMP_EMAIL  " \
                          "   AND A.APVL_REQ_DIVS <> '99'" \
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
                          "     , CASE WHEN A.APVL_REQ_DIVS = '01' THEN '연장근무' WHEN A.APVL_REQ_DIVS = '02' THEN '휴일근무' WHEN A.APVL_REQ_DIVS = '03' THEN '연차결재' WHEN A.APVL_REQ_DIVS = '04' THEN '반차결재' ELSE '' END APVL_REQ_NM  " \
                          "     , CASE WHEN A.TH1_APRV_STUS = '01' AND NVL(A.TH2_APRV_STUS, '01') = '01' THEN '미승인'" \
                          "            WHEN A.TH1_APRV_STUS = '02' AND NVL(A.TH2_APRV_STUS, '01') = '01' THEN '1차승인'" \
                          "            WHEN A.TH1_APRV_STUS = '02' AND NVL(A.TH2_APRV_STUS, '01') = '02' THEN '2차승인'" \
                          "            WHEN A.TH1_APRV_STUS = '03'  OR NVL(A.TH2_APRV_STUS, '01') = '03' THEN '반려'" \
                          "            ELSE '확인필요' END APRV_STUS_NM" \
                          "     , NVL(A.APVL_REQ_DT, '') APVL_REQ_DT " \
                          "     , CONCAT(NVL(A.WRK_REQ_RSN, ''), NVL(A.HOLI_REQ_RSN, '')) WRK_REQ_RSN " \
                          "     , NVL(A.TH1_APRV_STUS, '') AS TH1_APRV_STUS" \
                          "     , NVL(A.TH2_APRV_STUS, '') AS TH2_APRV_STUS" \
                          "     , CASE WHEN A.APVL_REQ_DIVS = '03'" \
                          "            THEN IFNULL(CONCAT(A.HOLI_TERM1, ' ~ ', A.HOLI_TERM2), '') " \
                          "            ELSE ''" \
                          "        END AS YEONCHA" \
                          "     , CASE WHEN A.APVL_REQ_DIVS = '04'" \
                          "            THEN CONCAT(IFNULL(A.HOLI_TERM2, ''), '(', CASE WHEN A.HDO_KD_CD = '01' THEN '오전' ELSE '오후' END, ')') " \
                          "            ELSE ''" \
                          "        END AS BANCHA" \
                          "     , NVL(A.TH1_APRV_NM, '') AS TH1_APRV_NM " \
                          "     , NVL(A.TH2_APRV_NM, '') AS TH2_APRV_NM " \
                          "  FROM TB_NEW_APVL_REQ_MGMT_M A, TB_EMP_MGMT C " \
                          " WHERE A.EMP_EMAL_ADDR = C.EMP_EMAIL  " \
                          "   and A.APVL_REQ_DIVS <> '99'"

                    if email == empPr:
                        sql=sql+"   AND A.TH1_APRV_NM = '" + email + "' AND A.TH1_APRV_STUS = '" + apvlStusDivs + "'  "
                    elif email == empGm:
                        sql=sql+"   AND A.TH2_APRV_NM = '" + email + "' AND A.TH1_APRV_STUS = '02' AND A.TH2_APRV_STUS = '" + apvlStusDivs + "'  "

                    sql=sql+" ORDER BY APVL_REQ_DT ASC "

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
        #mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
        #                                charset='utf8', autocommit=False)
        mysql_con = getMariaConn()

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
        #mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
        #                                charset='utf8', autocommit=False)
        mysql_con = getMariaConn()

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
        mysql_con = getMariaConn()
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
        mysql_con = getMariaConn()
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT C.CMM_CD AS DEPT_CD " \
                      "     , C.CMM_CD_NAME AS DEPT_NAME " \
                      "     , (SELECT E.EMP_NAME FROM TB_EMP_MGMT E WHERE E.EMP_ID = C.GM_ID) AS DEPT_GM_NAME " \
                      "     , GM_ID AS DEPT_GM_EMAIL " \
                      "  FROM TB_CMM_CD_DETL C " \
                      " WHERE C.CMM_CD_GRP_ID = 'SLIN_BZDP'" \
                      "   AND C.CMM_CD = (" \
                      "                   SELECT DEPT_CD " \
                      "                     FROM TB_EMP_MGMT " \
                      "                    WHERE EMP_EMAIL = '" + data["email"] + "'" \
                      "                  )"

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
        mysql_con = getMariaConn()
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT D.CMM_CD      AS DEPT_CD " \
                      "     , D.CMM_CD_NAME AS DEPT_NAME " \
                      "     , D.EMP_ID      AS DEPT_PR_EMAIL " \
                      "     , (SELECT XX.EMP_NAME FROM TB_EMP_MGMT XX WHERE XX.EMP_ID = D.EMP_ID) AS DEPT_PR_NAME " \
                      "  FROM TB_CMM_CD_DETL D " \
                      " WHERE D.CMM_CD_GRP_ID = 'SLIN_BZDP' " \
                      "   AND D.CMM_CD = ( " \
                      "                   SELECT X.DEPT_CD " \
                      "                     FROM TB_EMP_MGMT X  " \
                      "                    WHERE X.EMP_EMAIL = '" + data["email"] + "' " \
                      "                  ) "

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
        mysql_con = getMariaConn()
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
        logging.debug('================== duplApvlReqCnt App Start ==================')
        logging.debug(data)
        logging.debug(data["email"])
        logging.debug(data["wrkDt"])
        logging.debug(data["wrkSeq"])
        logging.debug(data["holiTerm2"])
        logging.debug(data["jobStrtTm"])
        logging.debug(data["jobEndTm"])
        logging.debug('================== duplApvlReqCnt App End ==================')

        #requirements pymysql import 후 커넥트 사용
        mysql_con = getMariaConn()
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT COUNT(*) AS APVL_REQ_CNT" \
                      "     , CASE WHEN APVL_REQ_DIVS = '01' THEN '연장근무' " \
                      "            WHEN APVL_REQ_DIVS = '02' THEN '휴일근무' " \
                      "            WHEN APVL_REQ_DIVS = '03' THEN '연차결재' " \
                      "            WHEN APVL_REQ_DIVS = '04' THEN '반차결재' " \
                      "            ELSE '' " \
                      "       END APVL_DIVS   " \
                      "  FROM TB_NEW_APVL_REQ_MGMT_M " \
                      " WHERE APVL_REQ_DIVS <> '99'" \
                      "   AND EMP_EMAL_ADDR = '" + data["email"] + "' " \
                      "   AND WRK_DT = '"+ data["wrkDt"] +"' " \
                      "   AND ('" + data["jobStrtTm"] + "' BETWEEN JOB_STRT_TM AND JOB_END_TM" \
                      "    OR  '" + data["jobEndTm"] + "' BETWEEN JOB_STRT_TM AND JOB_END_TM) "

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


class duplApvlYryReqCnt(Resource):  # Mariadb 연결 진행
    def get(self):

        data = request.get_json()
        logging.debug('================== duplApvlYryReqCnt App Start ==================')
        logging.debug(data)
        logging.debug(data["email"])
        logging.debug(data["wrkDt"])
        logging.debug(data["wrkSeq"])
        logging.debug(data["holiTerm2"])
        logging.debug('================== duplApvlYryReqCnt App End ==================')

        # requirements pymysql import 후 커넥트 사용
        mysql_con = getMariaConn()
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT COUNT(*) AS APVL_REQ_CNT" \
                      "     , CASE WHEN APVL_REQ_DIVS = '01' THEN '연장근무' " \
                      "            WHEN APVL_REQ_DIVS = '02' THEN '휴일근무' " \
                      "            WHEN APVL_REQ_DIVS = '03' THEN '연차결재' " \
                      "            WHEN APVL_REQ_DIVS = '04' THEN '반차결재' " \
                      "            ELSE '' " \
                      "       END APVL_DIVS   " \
                      "  FROM TB_NEW_APVL_REQ_MGMT_M " \
                      " WHERE APVL_REQ_DIVS <> '99'" \
                      "   AND EMP_EMAL_ADDR = '" + data["email"] + "' " \
                      "   AND APVL_REQ_DIVS in ('03', '04') " \
                      "   AND WRK_DT = '" + data["wrkDt"] + "' " \
                      "   AND (WRK_DT BETWEEN '"       + data["wrkDt"] + "' AND '"+ data["holiTerm2"] +"'" \
                      "       OR '" + data["wrkDt"] + "' BETWEEN HOLI_TERM1 AND HOLI_TERM2) "

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


class duplWrkCnt(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        #requirements pymysql import 후 커넥트 사용
        mysql_con = getMariaConn()
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql =   "SELECT COUNT(*) AS WRK_CNT " \
                        "FROM   TB_WRK_TM_MGMT_M    " \
                        "WHERE  EMP_EMAL_ADDR    = '" + data["email"]  + "' " \
                        "AND    WRK_DT 			 = '" + data["wrkDt"]  + "' "

                logging.debug("duplWrkCnt SQL문" + sql)
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


class wrkTm(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        #requirements pymysql import 후 커넥트 사용
        mysql_con = getMariaConn()
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql =   "SELECT NVL(DATE_FORMAT(NGHT_WRK_STRT_TM , '%H:%i'),'-') AS NGHT_WRK_STRT_TM " \
                        "     , NVL(DATE_FORMAT(JOB_END_TM       , '%H:%i'),'-') AS JOB_END_TM  " \
                        "FROM   TB_WRK_TM_MGMT_M " \
                        "WHERE  EMP_EMAL_ADDR    = '" + data["email"] + "' " \
                        "AND    WRK_DT 			 = '" + data["wrkDt"] + "' "

                logging.debug("wrkTm SQL문" + sql)
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

        logging.debug('================== App Start ==================')
        logging.debug(data)
        logging.debug('===============================================')
        #requirements pymysql import 후 커넥트 사용
        mysql_con = getMariaConn()
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "            SELECT NVL(A.EMP_EMAL_ADDR,'') EMP_EMAIL " \
                      "                 , NVL(D.EMP_NAME,'') EMP_NAME " \
                      "                 , NVL(A.TH1_APRV_NM,'') TH1_APRV_NM " \
                      "                 , NVL(B.EMP_NAME,'') TH1_APRV_NAME " \
                      "                 , NVL(A.TH2_APRV_NM,'') TH2_APRV_NM " \
                      "                 , NVL(E.EMP_NAME,'') TH2_APRV_NAME " \
                      "                 , NVL(C.EMP_EMAIL,'') REF_NM" \
                      "                 , NVL(C.EMP_NAME,'') REF_NAME" \
                      "                 , NVL(F.EMP_EMAIL,'') REF2_NM" \
                      "                 , NVL(F.EMP_NAME,'') REF2_NAME" \
                      "                 , DATE_FORMAT(A.APVL_REQ_DT, '%Y-%m-%d') APVL_REQ_DT" \
                      "                 , DATE_FORMAT(A.WRK_DT, '%Y-%m-%d') WRK_DT" \
                      "                 , DATE_FORMAT(A.JOB_STRT_TM, '%H:%i:%s') JOB_STRT_TM" \
                      "                 , DATE_FORMAT(A.JOB_END_TM, '%H:%i:%s') JOB_END_TM" \
                      "                 , CONCAT(NVL(A.WRK_REQ_RSN, ''), NVL(A.HOLI_REQ_RSN, '')) WRK_REQ_RSN" \
                      "                 , NVL(DATE_FORMAT(A.APVL_UPD_DT, '%Y-%m-%d'), '') APVL_UPD_DT" \
                      "                 , NVL(A.TH1_APRV_RSN,'') TH1_APRV_RSN " \
                      "                 , NVL(DATE_FORMAT(A.TH1_APRV_DT, '%Y-%m-%d'), '') TH1_APRV_DT" \
                      "                 , NVL(A.TH2_APRV_RSN,'') TH2_APRV_RSN " \
                      "                 , NVL(DATE_FORMAT(A.TH2_APRV_DT, '%Y-%m-%d'), '') TH2_APRV_DT" \
                      "                 , NVL(A.HOLI_TERM1, '') AS HOLI_TERM1 " \
                      "                 , NVL(A.HOLI_TERM2, '') AS HOLI_TERM2 " \
                      "                 , NVL(A.PTO_KD_CD, '') AS PTO_KD_CD " \
                      "                 , NVL(A.HDO_KD_CD, '') AS HDO_KD_CD " \
                      "                 , A.WRK_SEQ " \
                      "              FROM TB_NEW_APVL_REQ_MGMT_M A " \
                      "   LEFT OUTER JOIN TB_EMP_MGMT B " \
                      "                ON A.TH1_APRV_NM = B.EMP_EMAIL " \
                      "   LEFT OUTER JOIN TB_EMP_MGMT E " \
                      "                ON A.TH2_APRV_NM = E.EMP_EMAIL " \
                      "   LEFT OUTER JOIN TB_EMP_MGMT C " \
                      "                ON A.REF_NM = C.EMP_EMAIL " \
                      "   LEFT OUTER JOIN TB_EMP_MGMT F " \
                      "                ON A.REF2_NM = F.EMP_EMAIL " \
                      "   LEFT OUTER JOIN TB_EMP_MGMT D " \
                      "                ON A.EMP_EMAL_ADDR = D.EMP_EMAIL " \
                      "             WHERE A.EMP_EMAL_ADDR = '" + data["email"] + "'" \
                      "               AND A.WRK_SEQ = '" + data["wrkSeq"]     + "'" \
                      "               AND DATE_FORMAT(APVL_REQ_DT, '%Y-%m-%d') = '" + data["apvlReqDt"] + "'" \
                      "               AND '" + data["wrkDt"] + "' BETWEEN A.HOLI_TERM1 AND A.HOLI_TERM2"

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

class apvlReqWrkHistDetl(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        #requirements pymysql import 후 커넥트 사용
        mysql_con = getMariaConn()
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "            SELECT NVL(A.EMP_EMAL_ADDR,'') EMP_EMAIL " \
                      "                 , NVL(D.EMP_NAME,'') EMP_NAME " \
                      "                 , NVL(A.TH1_APRV_NM,'') TH1_APRV_NM " \
                      "                 , NVL(B.EMP_NAME,'') TH1_APRV_NAME " \
                      "                 , NVL(A.TH2_APRV_NM,'') TH2_APRV_NM " \
                      "                 , NVL(E.EMP_NAME,'') TH2_APRV_NAME " \
                      "                 , NVL(C.EMP_EMAIL,'') REF_NM" \
                      "                 , NVL(C.EMP_NAME,'') REF_NAME" \
                      "                 , NVL(F.EMP_EMAIL,'') REF2_NM" \
                      "                 , NVL(F.EMP_NAME,'') REF2_NAME" \
                      "                 , DATE_FORMAT(A.APVL_REQ_DT, '%Y-%m-%d') APVL_REQ_DT" \
                      "                 , DATE_FORMAT(A.WRK_DT, '%Y-%m-%d') WRK_DT" \
                      "                 , DATE_FORMAT(A.JOB_STRT_TM, '%H:%i:%s') JOB_STRT_TM" \
                      "                 , DATE_FORMAT(A.JOB_END_TM, '%H:%i:%s') JOB_END_TM" \
                      "                 , CONCAT(NVL(A.WRK_REQ_RSN, ''), NVL(A.HOLI_REQ_RSN, '')) WRK_REQ_RSN" \
                      "                 , NVL(DATE_FORMAT(A.APVL_UPD_DT, '%Y-%m-%d'), '') APVL_UPD_DT" \
                      "                 , NVL(A.TH1_APRV_RSN,'') TH1_APRV_RSN " \
                      "                 , NVL(DATE_FORMAT(A.TH1_APRV_DT, '%Y-%m-%d'), '') TH1_APRV_DT" \
                      "                 , NVL(A.TH2_APRV_RSN,'') TH2_APRV_RSN " \
                      "                 , NVL(DATE_FORMAT(A.TH2_APRV_DT, '%Y-%m-%d'), '') TH2_APRV_DT" \
                      "                 , NVL(A.HOLI_TERM1, '') AS HOLI_TERM1 " \
                      "                 , NVL(A.HOLI_TERM2, '') AS HOLI_TERM2 " \
                      "                 , NVL(A.PTO_KD_CD, '') AS PTO_KD_CD " \
                      "                 , NVL(A.HDO_KD_CD, '') AS HDO_KD_CD " \
                      "                 , A.WRK_SEQ " \
                      "              FROM TB_NEW_APVL_REQ_MGMT_M A " \
                      "   LEFT OUTER JOIN TB_EMP_MGMT B " \
                      "                ON A.TH1_APRV_NM = B.EMP_EMAIL " \
                      "   LEFT OUTER JOIN TB_EMP_MGMT E " \
                      "                ON A.TH2_APRV_NM = E.EMP_EMAIL " \
                      "   LEFT OUTER JOIN TB_EMP_MGMT C " \
                      "                ON A.REF_NM = C.EMP_EMAIL " \
                      "   LEFT OUTER JOIN TB_EMP_MGMT F " \
                      "                ON A.REF2_NM = F.EMP_EMAIL " \
                      "   LEFT OUTER JOIN TB_EMP_MGMT D " \
                      "                ON A.EMP_EMAL_ADDR = D.EMP_EMAIL " \
                      "             WHERE A.APVL_REQ_DIVS <> '99'" \
                      "               AND A.EMP_EMAL_ADDR = '" + data["email"]     + "'" \
                      "               AND A.WRK_SEQ = '" + data["wrkSeq"]     + "'" \
                      "               AND DATE_FORMAT(APVL_REQ_DT, '%Y-%m-%d') = '" + data["apvlReqDt"] + "'" \

                logging.debug("apvlReqWrkHistDetl SQL문 : " + sql)
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
        mysql_con = getMariaConn()
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "     WITH TMP_TM AS (SELECT    A.EMP_EMAL_ADDR " \
                      +"                             ,A.WRK_DT " \
                      +"                             ,NVL(DATE_FORMAT(A.JOB_STRT_TM, '%H:%i'),'-') AS JOB_STRT_TM " \
                      +"                             ,NVL(DATE_FORMAT(A.JOB_END_TM, '%H:%i'),'-') AS JOB_END_TM " \
                      +"                             ,'' AS NORM_WRK_TM " \
                      +"                             ,'' AS ALL_WRK_TM " \
                      +"                             ,'' AS APVL_REQ_DIVS " \
                      +"                             ,'' AS APVL_REQ_DT " \
                      +"                             ,'' AS APVL_LAST_APRV_DT " \
                      +"                             ,'' AS TH1_APRV_STUS " \
                      +"                             ,'' AS TH2_APRV_STUS " \
                      +"                             ,'' AS OVER_WRK_TM " \
                      +"                             ,NULL AS HOLI_TERM1 " \
                      +"                             ,'' AS HOLI_TERM2 " \
                      +"                         FROM TB_WRK_TM_MGMT_M A " \
                      +"                        WHERE 1 = 1 " \
                      + "                         AND A.EMP_EMAL_ADDR = '" + data["email"] + "'" \
                      + "                         AND A.WRK_DT LIKE '" + data["dt"] + "%')" \
                      +"     SELECT A.* " \
                      +"       FROM TMP_TM A" \
                      +"      UNION ALL" \
                      +"     SELECT A.EMP_EMAL_ADDR " \
                      +"	     ,A.WRK_DT " \
                      +"	     ,NVL(DATE_FORMAT(B.JOB_STRT_TM, '%H:%i'),'-') AS JOB_STRT_TM " \
                      +"	     ,NVL(DATE_FORMAT(B.JOB_END_TM, '%H:%i'),'-') AS JOB_END_TM " \
                      +"	     ,'' AS NORM_WRK_TM " \
                      +"	     ,'' AS ALL_WRK_TM " \
                      +"	     ,NVL(B.APVL_REQ_DIVS, 'N\A') AS APVL_REQ_DIVS " \
                      +"	     ,NVL(B.APVL_REQ_DT, 'N\A') AS APVL_REQ_DT " \
                      +"	     ,NVL(B.APVL_LAST_APRV_DT, 'N\A') AS APVL_LAST_APRV_DT " \
                      +"	     ,NVL(B.TH1_APRV_STUS, 'N\A') AS TH1_APRV_STUS " \
                      +"	     ,NVL(B.TH2_APRV_STUS, 'N\A') AS TH2_APRV_STUS " \
                      +"	     ,'' AS OVER_WRK_TM " \
                      +"         ,B.HOLI_TERM1 AS HOLI_TERM1 " \
                      +"         ,B.HOLI_TERM2 AS HOLI_TERM2 " \
                      +"	 FROM TMP_TM A " \
                      +"	 JOIN TB_NEW_APVL_REQ_MGMT_M B" \
                      +"	   ON A.WRK_DT = B.WRK_DT" \
                      +"	  AND A.EMP_EMAL_ADDR = B.EMP_EMAL_ADDR " \
                      +"	  AND B.APVL_REQ_DIVS <> '99'" \
                      +"	  ORDER BY WRK_DT,JOB_STRT_TM, HOLI_TERM1 IS NULL ASC" \

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
        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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
        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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
        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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
        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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
        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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



        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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


        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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
        #params = request.get_json()
        logger.info("App Parameters Start")
        logger.info(params)
        logger.info(type(params))
        logger.info("App Parameters End")

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        email           = params['email']
        apvlDivs        = params['apvlDivs']
        apvlReqDivs     = params['apvlReqDivs']
        ptoKdCd         = params['ptoKdCd']
        hdoKdCd         = params['hdoKdCd']
        jobStrtTm       = params['jobStrtTm']
        jobEndTm        = params['jobEndTm']
        holiTerm1       = params['holiTerm1']
        holiTerm2       = params['holiTerm2']
        wrkDt           = params['wrkDt']
        wrkSeq          = params['wrkSeq']
        wrkTme          = params['wrkTme']
        wrkReqRsn       = params['wrkReqRsn']
        th1AprvStus     = params['th1AprvStus']
        th1AprvNm       = params['th1AprvNm']
        th2AprvStus     = params['th2AprvStus']
        th2AprvNm       = params['th2AprvNm']
        refNm           = params['refNm']
        ref2Nm          = params['ref2Nm']
        #emerCtpl        = params['emerCtpl']
        holiDays        = params['holiDays']

        logging.debug("====Param data====")

        logging.debug("email        = " + email)
        logging.debug("apvlDivs     = " + apvlDivs)
        logging.debug("apvlReqDivs  = " + apvlReqDivs)
        logging.debug("ptoKdCd      = " + ptoKdCd)
        logging.debug("hdoKdCd      = " + hdoKdCd)
        logging.debug("jobStrtTm    = " + jobStrtTm)
        logging.debug("jobEndTm     = " + jobEndTm)
        logging.debug("holiTerm1    = " + holiTerm1)
        logging.debug("holiTerm2    = " + holiTerm2)
        logging.debug("wrkDt        = " + wrkDt)
        logging.debug("wrkSeq       = " + wrkSeq)
        logging.debug("wrkTme       = " + wrkTme)
        logging.debug("wrkReqRsn    = " + wrkReqRsn)
        logging.debug("th1AprvStus  = " + th1AprvStus)
        logging.debug("th1AprvNm    = " + th1AprvNm)
        logging.debug("th2AprvStus  = " + th2AprvStus)
        logging.debug("th2AprvNm    = " + th2AprvNm)
        logging.debug("refNm        = " + refNm)
        logging.debug("ref2Nm       = " + ref2Nm)
        #logging.debug("emerCtpl     = " + emerCtpl)
        logging.debug("holiDays     = " + holiDays)

        logging.debug("========== 연차 시작일 / 종료일 사이 평일 추출 ==========")
        strtDt = date(int(holiTerm1.split('-')[0]), int(holiTerm1.split('-')[1]), int(holiTerm1.split('-')[2]))
        endDt  = date(int(holiTerm2.split('-')[0]), int(holiTerm2.split('-')[1]), int(holiTerm2.split('-')[2]))
        delta  = endDt - strtDt
        datelist = []

        # 시작일 / 종료일 사이 평일 
        for i in range(delta.days + 1):
            if ((strtDt + timedelta(days=i)).weekday() < 5):
                datelist.append((strtDt + timedelta(days=i)).isoformat())

        logging.debug(datelist)
        logging.debug("=========================================================")


        # requirements pymysql import 후 커넥트 사용
        mysql_con = getMariaConn()
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:

                # 쿼리문 실행
                sql1 = "INSERT INTO TB_NEW_APVL_REQ_MGMT_M (" \
                                                      "`EMP_EMAL_ADDR`," \
                                                      "`APVL_REQ_DIVS`," \
                                                      "`PTO_KD_CD`," \
                                                      "`HDO_KD_CD`," \
                                                      "`WRK_DT`," \
                                                      "`WRK_SEQ`," \
                                                      "`JOB_STRT_TM`," \
                                                      "`JOB_END_TM`," \
                                                      "`HOLI_TERM1`," \
                                                      "`HOLI_TERM2`," \
                                                      "`WRK_TME`," \
                                                      "`HOLI_REQ_RSN`," \
                                                      "`APVL_REQ_DT`," \
                                                      "`TH1_APRV_STUS`," \
                                                      "`TH1_APRV_NM`," \
                                                      "`TH2_APRV_STUS`," \
                                                      "`TH2_APRV_NM`," \
                                                      "`REF_NM`," \
                                                      "`REF2_NM`," \
                                                      "`APVL_LAST_APRV_DT`)" \
                                            " VALUES (   '" + email       + "'"\
                                                      ", '" + apvlReqDivs + "'"\
                                                      ", '" + ptoKdCd + "'"\
                                                      ", '" + hdoKdCd + "'"\
                                                      ", '" + wrkDt       + "'" \
                                                      ", (SELECT NVL(MAX(WRK_SEQ), 0)+1" \
                                                      "     FROM TB_NEW_APVL_REQ_MGMT_M as WRKSEQ" \
                                                      "    WHERE EMP_EMAL_ADDR = '" + email + "'" \
                                                      "      AND WRK_DT = '" + wrkDt + "'" \
                                                      "  ) " \
                                                      ", '" + jobStrtTm   + "'"\
                                                      ", '" + jobEndTm    + "'"\
                                                      ", '" + holiTerm1   + "'"\
                                                      ", '" + holiTerm2   + "'"\
                                                      ", '" + wrkTme      + "'"\
                                                      ", '" + wrkReqRsn   + "'"\
                                                      ",      NOW()" \
                                                      ", '" + th1AprvStus + "'"\
                                                      ", '" + th1AprvNm   + "'"\
                                                      ", '" + th2AprvStus + "'"\
                                                      ", '" + th2AprvNm   + "'"\
                                                      ", '" + refNm       + "'"\
                                                      ", '" + ref2Nm      + "'"\
                                                      ",      NOW()" \
                                                      ") ON DUPLICATE KEY " \
                    "UPDATE   `APVL_REQ_DIVS`   = '" + apvlReqDivs + "'"\
                    "		, `PTO_KD_CD`		= '" + ptoKdCd + "'"\
                    "		, `HDO_KD_CD` 		= '" + hdoKdCd + "'"\
                    "		, `JOB_STRT_TM`     = '" + jobStrtTm   + "'"\
                    "		, `JOB_END_TM`      = '" + jobEndTm    + "'"\
                    "		, `HOLI_TERM1`      = '" + holiTerm1   + "'"\
                    "		, `HOLI_TERM2`      = '" + holiTerm2   + "'"\
                    "		, `WRK_TME`         = '" + wrkTme      + "'"\
                    "		, `HOLI_REQ_RSN`    = '" + wrkReqRsn   + "'"\
                    "		, `APVL_REQ_DT`     = NOW()" \
                    "		, `TH1_APRV_STUS`   = '" + th1AprvStus + "'"\
                    "		, `TH1_APRV_NM`     = '" + th1AprvNm   + "'"\
                    "		, `TH2_APRV_STUS`   = '" + th2AprvStus + "'"\
                    "		, `TH2_APRV_NM`     = '" + th2AprvNm   + "'"\
                    "		, `REF_NM`          = '" + refNm       + "'"\
                    "		, `REF2_NM`         = '" + ref2Nm      + "'"\
                    "		, `APVL_LAST_APRV_DT` = NOW()"
                logger.info(sql1)
                cursor.execute(sql1)

                sql3 = "UPDATE TB_YRY_MGMT_M" \
                       "   SET USE_YRY_DAYS = USE_YRY_DAYS + %s" \
                       " WHERE EMP_EMAL_ADDR = %s" \

                logger.info(sql3)
                cursor.execute(sql3, (holiDays, email))

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


class saveYryApvlCncl(Resource):  # Mariadb 연결 진행
    def post(self):

        params = json.loads(request.data)
        # params = request.get_json()
        logger.info("App Parameters Start")
        logger.info(params)
        logger.info(type(params))
        logger.info("App Parameters End")

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        email = params['email']
        apvlReqDivs = params['apvlReqDivs']
        wrkDt = params['wrkDt']
        wrkSeq = params['wrkSeq']
        logging.debug("====Param data====")

        logging.debug("email        = " + email)
        logging.debug("apvlReqDivs  = " + apvlReqDivs)
        logging.debug("wrkDt        = " + wrkDt)
        logging.debug("wrkSeq       = " + wrkSeq)

        # requirements pymysql import 후 커넥트 사용
        mysql_con = getMariaConn()
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql1 = "UPDATE TB_NEW_APVL_REQ_MGMT_M " \
                       "   SET APVL_REQ_DIVS = '"+apvlReqDivs+"'" \
                       " WHERE EMP_EMAL_ADDR = '"+email+"'" \
                       "   AND WRK_DT        = '"+wrkDt+"'" \
                       "   AND WRK_SEQ       = '"+wrkSeq+"'"
                logger.info(sql1)
                cursor.execute(sql1)
                mysql_con.commit()
        except Exception as e:
            logger.info("에러!!!!!!!!!!!!!!!!!!!!!!!" + e)
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
        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:

                sql1 =  "UPDATE TB_APVL_REQ_MGMT_M    " \
                        "   SET JOB_STRT_TM  	= %s  " \
                        "     , APVL_UPD_DT  	= NOW()  " \
                        " WHERE EMP_EMAL_ADDR 	= %s  " \
                        "   AND WRK_DT 			= %s  " \
                        "   AND TH1_APRV_STUS 	= '01' " \
                        "   AND JOB_STRT_TM 	= (  " \
                        "						   SELECT NGHT_WRK_STRT_TM  " \
                        "						     FROM TB_WRK_TM_MGMT_M  " \
                        "						    WHERE EMP_EMAL_ADDR  = %s  " \
                        "						      AND WRK_DT 		 = %s  " \
                        "						   ) "
                logger.info(sql1)
                cursor.execute(sql1, (tm, email, dt, email, dt))

                # 쿼리문 실행
                sql2 = "INSERT INTO TB_WRK_TM_MGMT_M( `EMP_EMAL_ADDR` " \
                      ",`WRK_DT` " \
                      ",`JOB_STRT_TM` " \
                      ") VALUES( %s ,%s ,%s ) " \
                      "ON DUPLICATE KEY " \
                      "UPDATE `JOB_STRT_TM` = %s"
                logger.info(sql2)
                cursor.execute(sql2, (email, dt, tm, tm))

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
        nghtWrkStrtTm = params['nghtWrkStrtTm']
        normWrkTm = params['normWrkTm']
        overWrkTm = params['overWrkTm']
        allWrkTm = params['allWrkTm']


        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 주말근무케이스
                if normWrkTm == "000000" and allWrkTm != "000000":
                    # 쿼리문 실행
                    sql = "UPDATE TB_WRK_TM_MGMT_M " \
                          "   SET JOB_END_TM  = %s " \
                          "      ,NGHT_WRK_STRT_TM = %s " \
                          "      ,HLDY_WRK_TM = %s " \
                          "      ,ALL_WRK_TM  = %s " \
                          "   WHERE EMP_EMAL_ADDR = %s " \
                          "   AND WRK_DT = %s "
                    logger.info(sql)
                    cursor.execute(sql, (tm, nghtWrkStrtTm, overWrkTm, allWrkTm, email, dt))

                else:
                    # 쿼리문 실행, 주말 외
                    sql = "UPDATE TB_WRK_TM_MGMT_M " \
                          "   SET JOB_END_TM  = %s " \
                          "      ,NGHT_WRK_STRT_TM = %s " \
                          "      ,NORM_WRK_TM = %s " \
                          "      ,NGHT_WRK_TM = %s " \
                          "   WHERE EMP_EMAL_ADDR = %s " \
                          "   AND WRK_DT = %s "
                    logger.info(sql)
                    cursor.execute(sql, (tm, nghtWrkStrtTm, normWrkTm, overWrkTm, email, dt))

                # 수정하려는 날짜의 미승인 결재 요청 건이 있을 경우, 해당 record 수정 2022-06-28 불필요 로직으로 보이며 제거
                # sql = "UPDATE TB_APVL_REQ_MGMT_M " \
                #       "   SET JOB_STRT_TM  	    = %s " \
                #       "     , JOB_END_TM 	    = %s " \
                #       "     , WRK_TME 		    = %s " \
                #       "     , APVL_UPD_DT 	    = NOW()" \
                #       " WHERE EMP_EMAL_ADDR     = %s " \
                #       "   AND WRK_DT 		    = %s " \
                #       "   AND TH1_APRV_STUS     = '01' "
                # logger.info(sql)
                # cursor.execute(sql, (nghtWrkStrtTm, tm, overWrkTm, email, dt))
                mysql_con.commit()
        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been saved successfully"
        }

        return jsonify(retJson)


class updateWrkTimeConfirm(Resource):  # 근무시간 확정
    def post(self):

        params = json.loads(request.data)
        logger.info("App Parameters Start")
        logger.info(params['email'])
        logger.info("App Parameters End")

        email = params['email']
        dept = params['dept']
        th1AprvNm = params['th1AprvNm']
        wrkDt = params['wrkDt']

        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "UPDATE TB_WRK_TM_MGMT_M M " \
                      "   SET M.APRV_STUS = '1' " \
                      "     , M.APRV_NM   = '" + th1AprvNm + "' " \
                      "     , M.APRV_DT   = NOW() " \
                      "   WHERE 1=1 " \
                      "     AND SUBSTR(M.WRK_DT, 1, 7) = '" + wrkDt + "'"
                if email != "" and email != "00":
                    sql += "   AND M.EMP_EMAL_ADDR = '" + email + "' "
                if dept != ""  and dept  != "00":
                    sql += "   AND EXISTS ( SELECT 'X' "
                    sql += "                  FROM TB_EMP_MGMT E "
                    sql += "                 WHERE E.EMP_EMAIL = M.EMP_EMAL_ADDR "
                    sql += "                   AND E.DEPT_CD = '" + dept + "'"
                    sql += "              ) "
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


class insertWrkTimeGen(Resource):  # 근무시간 생성
    def post(self):

        params = json.loads(request.data)
        wrkDt = params['wrkDt']
        logger.info("App Parameters Start")
        logger.info("wrkDt : "+wrkDt)
        logger.info("App Parameters End")

        # requirements pymysql import 후 커넥트 사용
        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "INSERT INTO TB_WRK_TM_MGMT_M " \
                      "SELECT *" \
                      "  FROM (" \
                      "         SELECT E.EMP_ID " \
                      "              , D.YMD_DATE " \
                      "              , E.JOB_STRT_TM " \
                      "              , E.JOB_END_TM " \
                      "              , E.JOB_END_TM AS NGHT_WRK_STRT_TM " \
                      "              , '080000' AS NORM_WRK_TM " \
                      "              , '000000' AS HLDY_WRK_TM " \
                      "              , '000000' AS NGHT_WRK_TM " \
                      "              , '090000' AS ALL_WRK_TM " \
                      "              , '60'     AS REST_TM " \
                      "              , '0'      AS DINN_REST_TM " \
                      "              , NULL     AS APRV_STUS " \
                      "              , NULL     AS APRV_NM " \
                      "              , NULL     AS APRV_DT " \
                      "              , NOW()    AS INSRT_DT " \
                      "              , NOW()    AS UPDT_DT " \
                      "           FROM TB_EMP_MGMT E " \
                      "              , TB_DATE D " \
                      "          WHERE D.ymd_date like '" + wrkDt + "%'"\
                      "            AND D.HOLY_GB = 'N'" \
                      "            AND E.WORK_YN = 'Y'" \
                      "       ) S " \
                      " ON DUPLICATE KEY " \
                      "UPDATE JOB_STRT_TM = S.JOB_STRT_TM"\
                      "     , JOB_END_TM  = S.JOB_END_TM"\
                      "     , NGHT_WRK_STRT_TM = S.NGHT_WRK_STRT_TM "\
                      "	    , NORM_WRK_TM = S.NORM_WRK_TM"\
                      "	    , HLDY_WRK_TM = S.HLDY_WRK_TM"\
                      "	    , NGHT_WRK_TM = S.NGHT_WRK_TM"\
                      "     , ALL_WRK_TM = S.ALL_WRK_TM"\
                      "     , REST_TM = S.REST_TM"\
                      "     , DINN_REST_TM = S.DINN_REST_TM"\
                      "     , APRV_STUS = S.APRV_STUS"\
                      "     , APRV_NM = S.APRV_NM"\
                      "     , APRV_DT = S.APRV_DT"\
                      "     , UPDT_DT = S.UPDT_DT "

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

class yryUseDays(Resource): # Mariadb 연결 진행
    def get(self):

        # get data
        data = request.get_json()

        #requirements pymysql import 후 커넥트 사용
        mysql_con = getMariaConn()
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

        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT " \
                      "CMM_CD_GRP_ID, CMM_CD, CMM_CD_NAME " \
                      "FROM TB_CMM_CD_DETL A " \
                      "WHERE CMM_CD_GRP_ID = '" + data["grp_id"] + "'" \
                      "  AND USE_YN = 'Y'"
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

        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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
                      "      ,(SELECT CASE WHEN DOW_DIVS_CD = '01' THEN '일'" \
                      "                    WHEN DOW_DIVS_CD = '02' THEN '월'" \
                      "                    WHEN DOW_DIVS_CD = '03' THEN '화'" \
                      "                    WHEN DOW_DIVS_CD = '04' THEN '수'" \
                      "                    WHEN DOW_DIVS_CD = '05' THEN '목'" \
                      "                    WHEN DOW_DIVS_CD = '06' THEN '금'" \
                      "                    WHEN DOW_DIVS_CD = '07' THEN '토'" \
		              "                    ELSE ''" \
					  "	                    END DOW_DT" \
 		              "          FROM TB_DT_INFO" \
			          "         WHERE DT = NVL(A.WRK_DT, B.WRK_DT)" \
		              "       ) DOW" \
                      "      ,(SELECT D.CMM_CD_NAME" \
                      "		     FROM TB_CMM_CD_DETL D" \
                      "		         ,TB_EMP_MGMT E" \
                      "			WHERE D.CMM_CD_GRP_ID = 'SLIN_BZDP'" \
                      "			  AND D.CMM_CD = E.DEPT_CD" \
                      "			  AND E.EMP_EMAIL = NVL(A.EMP_EMAL_ADDR, B.EMP_EMAL_ADDR)) DEPT_NAME" \
                      "	     ,(SELECT C.EMP_NAME " \
                      "	         FROM TB_EMP_MGMT C" \
                      "	        WHERE C.EMP_EMAIL = NVL(A.EMP_EMAL_ADDR, B.EMP_EMAL_ADDR)) OCEM_NAME" \
                      "      ,NVL(A.REST_TM, '') REST_TM" \
                      "      ,NVL(A.DINN_REST_TM, '') DINN_REST_TM" \
                      "      ,CASE WHEN B.EMP_EMAL_ADDR IS NULL AND (A.HLDY_WRK_TM != '000000' OR A.NGHT_WRK_TM != '000000') THEN '야근(미승인)'" \
                      "            WHEN B.APVL_REQ_DIVS IS NOT NULL THEN (SELECT F.CMM_CD_NAME" \
                      "                                                     FROM TB_CMM_CD_DETL F" \
                      "      										       WHERE F.CMM_CD_GRP_ID = 'APVL_DIVS_CD'" \
                      "      				     						     AND F.CMM_CD = B.APVL_REQ_DIVS)" \
                      "      		ELSE '정상근무' END WRK_DIVS" \
                      "		 ,CASE WHEN B.EMP_EMAL_ADDR IS NULL AND (A.HLDY_WRK_TM != '000000' OR A.NGHT_WRK_TM != '000000') " \
                      "            THEN '미등록'" \
                      "            WHEN B.TH2_APRV_STUS = '02'" \
                      "            THEN '승인완료'" \
                      "            WHEN B.TH1_APRV_STUS = '02'" \
                      "            THEN '1차승인'" \
                      "            WHEN B.TH1_APRV_STUS = '03' OR B.TH2_APRV_STUS = '03'" \
                      "            THEN '반려'"\
                      "            WHEN B.TH1_APRV_STUS = '01'" \
                      "            THEN '미승인'"\
                      "            ELSE ''" \
                      "        END AS APVL_STUS" \
                      "		 ,NVL(NVL(A.JOB_STRT_TM, B.JOB_STRT_TM), '') AS WRK_STRT_TM" \
                      "		 ,NVL(NVL(A.JOB_END_TM, B.JOB_END_TM), '') AS WRK_END_TM" \
                      "      ,CASE WHEN NVL(B.PTO_KD_CD, 'X') IN ('01', '03') /*01 연차, 03 기타*/ " \
                      "            THEN CONCAT(SUBSTRING(B.WRK_TME, 1, 2), ':', SUBSTRING(B.WRK_TME, 3, 2))" \
                      "            WHEN NVL(B.PTO_KD_CD, 'X') = '02' /*02 반차*/" \
                      "            THEN CONCAT(SUBSTRING(DATE_SUB(STR_TO_DATE(NVL(A.ALL_WRK_TM, '000000'), '%H%i%s'), INTERVAL A.REST_TM + A.DINN_REST_TM MINUTE), 1, 2), ':', SUBSTRING(DATE_SUB(STR_TO_DATE(NVL(A.ALL_WRK_TM, '000000'), '%H%i%s'), INTERVAL A.REST_TM + A.DINN_REST_TM MINUTE), 4, 2))" \
                      "            ELSE CONCAT(SUBSTRING(DATE_SUB(DATE_ADD(STR_TO_DATE(NVL(A.ALL_WRK_TM, '000000'), '%H%i%s'), INTERVAL TIME_TO_SEC(STR_TO_DATE(LPAD(NVL(B.WRK_TME, A.NGHT_WRK_TM), 6, '0'), '%H%i%s')) SECOND), INTERVAL A.REST_TM + A.DINN_REST_TM MINUTE), 1, 2), ':', SUBSTRING(DATE_SUB(DATE_ADD(STR_TO_DATE(NVL(A.ALL_WRK_TM, '000000'), '%H%i%s'), INTERVAL TIME_TO_SEC(STR_TO_DATE(LPAD(NVL(B.WRK_TME, A.NGHT_WRK_TM), 6, '0'), '%H%i%s')) SECOND), INTERVAL A.REST_TM + A.DINN_REST_TM MINUTE), 4, 2))" \
                      "        END AS ALL_WRK_TM"\
                      "      ,CASE WHEN B.EMP_EMAL_ADDR IS NULL AND (A.HLDY_WRK_TM != '000000' OR A.NGHT_WRK_TM != '000000') THEN 'N'" \
                      "            ELSE 'Y' END APVL_REQ_YN" \
                      "      ,CASE WHEN B.APVL_REQ_DIVS IN ('01', '02') AND NVL(NVL(B.WRK_TME, A.NGHT_WRK_TM), '') != '' AND NVL(NVL(B.WRK_TME, A.NGHT_WRK_TM), '') != '000000' " \
                      "            THEN CONCAT(SUBSTRING(STR_TO_DATE(NVL(B.WRK_TME, A.NGHT_WRK_TM), '%H%i%s'), 1, 2), ':', SUBSTRING(STR_TO_DATE(NVL(B.WRK_TME, A.NGHT_WRK_TM), '%H%i%s'), 4, 2))" \
                      "            ELSE ''" \
                      "             END NGHT_WRK_YN" \
                      "     , CASE WHEN B.APVL_REQ_DIVS IN ('01', '02') AND DATE_SUB(STR_TO_DATE(DATE_FORMAT(CASE WHEN NVL(B.APVL_REQ_DIVS,'') = '' THEN A.JOB_END_TM ELSE B.JOB_END_TM END, '%H%i%s'), '%H%i%s'), INTERVAL STR_TO_DATE('220000', '%H%i%s') DAY_SECOND) > 0 " \
                      "            THEN CONCAT(SUBSTRING(NVL(DATE_SUB(STR_TO_DATE(DATE_FORMAT(CASE WHEN NVL(B.APVL_REQ_DIVS,'') = '' THEN A.JOB_END_TM ELSE B.JOB_END_TM END, '%H%i%s'), '%H%i%s'), INTERVAL STR_TO_DATE('220000', '%H%i%s') DAY_SECOND), ''), 1, 2), ':', SUBSTRING(NVL(DATE_SUB(STR_TO_DATE(DATE_FORMAT(CASE WHEN NVL(B.APVL_REQ_DIVS,'') = '' THEN A.JOB_END_TM ELSE B.JOB_END_TM END, '%H%i%s'), '%H%i%s'), INTERVAL STR_TO_DATE('220000', '%H%i%s') DAY_SECOND), ''), 4, 2))" \
                      "            ELSE '' " \
                      "        END AS NGHT_SFT_YN" \
                      "      ,CASE WHEN NVL(A.HLDY_WRK_TM, '') != '' AND NVL(A.HLDY_WRK_TM, '') != '000000' " \
                      "            THEN CONCAT(SUBSTRING(DATE_SUB(STR_TO_DATE(NVL(A.HLDY_WRK_TM, ''), '%H%i%s'), INTERVAL A.REST_TM + A.DINN_REST_TM MINUTE), 1, 2), ':', SUBSTRING(DATE_SUB(STR_TO_DATE(NVL(A.HLDY_WRK_TM, ''), '%H%i%s'), INTERVAL A.REST_TM + A.DINN_REST_TM MINUTE), 4, 2))" \
                      "            ELSE ''" \
                      "             END HLDY_WRK_YN" \
                      "      ,CASE WHEN PTO_KD_CD IS NOT NULL" \
                      "            THEN NVL(CONCAT(SUBSTRING(B.WRK_TME, 1, 2), ':', SUBSTRING(B.WRK_TME, 3, 2)),'')" \
                      "            ELSE ''" \
                      "        END AS PTO_KD_YN" \
                      "      ,CASE WHEN A.APRV_STUS = '1' THEN 'Y'" \
                      "            ELSE 'N'" \
                      "        END AS APRV_STUS" \
                      "      ,NVL(A.APRV_NM, '') AS APRV_NM" \
                      "      ,NVL((SELECT Z.EMP_NAME FROM TB_EMP_MGMT Z WHERE Z.EMP_EMAIL = A.APRV_NM), '') AS APRV_NAME" \
                      "      ,NVL(A.APRV_DT, '') AS APRV_DT" \
                      "  FROM TB_WRK_TM_MGMT_M A" \
                      "  LEFT OUTER JOIN" \
                      "       TB_APVL_REQ_MGMT_M B" \
                      "    ON A.EMP_EMAL_ADDR = B.EMP_EMAL_ADDR" \
                      "   AND (A.WRK_DT = B.WRK_DT OR A.WRK_DT BETWEEN B.HOLI_TERM1 AND B.HOLI_TERM2)" \
                      "   AND B.APVL_REQ_DIVS <> '99'" \
                      " WHERE SUBSTRING(A.WRK_DT, 1, 7) = '" + data["wrkDt"] + "'"
                if data["email"] != "":
                      sql += "    AND A.EMP_EMAL_ADDR = '" + data["email"] + "'" \

                if data["wrkDivs"] != "" and data["wrkDivs"] != "00" and data["wrkDivs"] != "05" and data["wrkDivs"] != "06":
                      sql += "    AND B.APVL_REQ_DIVS = '" + data["wrkDivs"] + "'" \

                if data["wrkDivs"] != "" and data["wrkDivs"] == "05":
                      sql += "    AND A.HLDY_WRK_TM = '000000'" \
                             "    AND A.NGHT_WRK_TM = '000000'" \
                             "    AND A.ALL_WRK_TM != '000000'" \

                if data["wrkDivs"] != "" and data["wrkDivs"] == "06":
                      sql += "    AND B.EMP_EMAL_ADDR IS NULL" \
                             "    AND (A.HLDY_WRK_TM != '000000' OR A.NGHT_WRK_TM != '000000')" \

                if data["dept"] != "" and data["dept"] != "00":
                      sql += "    AND A.EMP_EMAL_ADDR IN (SELECT H.EMP_EMAIL" \
                             "                              FROM TB_EMP_MGMT H" \
                             "                             WHERE H.DEPT_CD = '" + data["dept"] + "')"\

                logging.debug(sql + "*****************")
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



        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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
        mysql_con = getMariaConn()
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT EMP_ID" \
                      "     , EMP_PW" \
                      "     , AUTH_ID" \
                      "     , EMP_NAME" \
                      "     , DEPT_CD" \
                      "     , DATE_FORMAT(JOB_STRT_TM, '%H%i%s') AS JOB_STRT_TM" \
                      "     , DATE_FORMAT(JOB_END_TM, '%H%i%s') AS JOB_END_TM" \
                      "  FROM TB_EMP_MGMT " \
                      " WHERE EMP_EMAIL = '" + data["email"] + "'";

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
        mysql_con = getMariaConn()
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
        ipt_jobStrtTm = request.form['ipt_jobStrtTm']
        ipt_jobEndTm = request.form['ipt_jobEndTm']
        sessionId = request.form['sessionId']
        ipt_empEmail = ipt_empId;


        logging.debug("====Param data====")

        logging.debug("ipt_empId = " + ipt_empId)
        logging.debug("ipt_empEmail = " + ipt_empEmail)
        logging.debug("ipt_empPw = " + ipt_empPw)
        logging.debug("ipt_empAuthId = " + ipt_empAuthId)
        logging.debug("ipt_empNm = " + ipt_empNm)
        logging.debug("ipt_empDept = " + ipt_empDept)
        logging.debug("ipt_jobStrtTm = " + ipt_jobStrtTm)
        logging.debug("ipt_jobEndTm = " + ipt_jobEndTm)
        logging.debug("sessionId = " + sessionId)

        logging.debug("=====================")



        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)


        logging.debug("save Start")

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql= "UPDATE TB_EMP_MGMT SET EMP_PW = '"+ipt_empPw+"', " \
                                                "EMP_NAME = '"+ipt_empNm+"', " \
                                                "AUTH_ID = '"+ipt_empAuthId+"', " \
                                                "DEPT_CD = '"+ipt_empDept+"', " \
                                                "JOB_STRT_TM = '" + ipt_jobStrtTm + "', " \
                                                "JOB_END_TM = '" + ipt_jobEndTm + "', " \
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



        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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
        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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
        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:

                sql = "SELECT A.QNA_WR_NM ORIGIN_WR, B.QNA_NO,  B.QNA_ORIGIN_NO,  B.DATA_DEPTH, B.QNA_SORTS, B.QNA_TITLE,  B.QNA_MAIN,  B.QNA_WR_NM , B.QNA_RGS_DATE, B.QNA_DEL_YN, C.EMP_NAME " \
                      "FROM TB_QNA_TEST  A, TB_QNA_TEST B, TB_EMP_MGMT C " \
                      "WHERE A.QNA_NO = B.QNA_ORIGIN_NO AND B.QNA_WR_NM = C.EMP_ID AND B.QNA_ORIGIN_NO NOT IN (SELECT QNA_NO FROM TB_QNA_TEST WHERE DATA_DEPTH = 0 AND QNA_DEL_YN = 'Y') " \
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
        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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
        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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



        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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
        mysql_con = getMariaConn()
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                if data["status"] == "R":
                    logging.debug("#######################R일때")
                    sql1 = "UPDATE TB_QNA_TEST SET QNA_CNT = QNA_CNT+1 WHERE QNA_NO = '" + data["number"] + "'"

                    logging.debug(sql1)
                    cursor.execute(sql1)
                    mysql_con.commit()

                sql2 = "SELECT A.*, B.ORIGIN_WR, C.EMP_NAME " \
                        "FROM TB_QNA_TEST A, " \
                        "(SELECT QNA_WR_NM ORIGIN_WR FROM TB_QNA_TEST A WHERE QNA_NO  = (SELECT QNA_ORIGIN_NO FROM TB_QNA_TEST WHERE QNA_NO = '"+ data["number"] +"')) B, " \
                        "(SELECT EMP_NAME FROM TB_EMP_MGMT WHERE EMP_ID = (SELECT QNA_WR_NM FROM TB_QNA_TEST WHERE QNA_NO = '"+ data["number"] +"')) C " \
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



        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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
        mysql_con = getMariaConn()
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



        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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



        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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



        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
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
        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "SELECT A.QNA_WR_NM ORIGIN_WR, B.*, C.EMP_NAME FROM TB_QNA_TEST  A, TB_QNA_TEST B, TB_EMP_MGMT C WHERE " \
                      "A.QNA_NO = B.QNA_ORIGIN_NO AND B.QNA_WR_NM = C.EMP_ID AND " \
                      "B.QNA_ORIGIN_NO NOT IN (SELECT QNA_NO FROM TB_QNA_TEST WHERE DATA_DEPTH = 0 AND QNA_DEL_YN = 'Y') AND " \
                      "B.QNA_ORIGIN_NO IN(SELECT QNA_NO FROM TB_QNA_TEST AA, TB_EMP_MGMT CC " \
		              "WHERE AA.QNA_WR_NM = CC.EMP_ID AND AA.DATA_DEPTH = '0' AND ("

                if option == "00" : #제목
                    sql += "AA.QNA_TITLE LIKE '%"+ keyword +"%'"
                if option == "01" : #내용
                    sql += "AA.QNA_MAIN LIKE '%"+ keyword +"%'"
                if option == "02" : #제목+내용
                    sql += "AA.QNA_TITLE LIKE '%"+ keyword +"%' OR AA.QNA_MAIN LIKE '%"+ keyword +"%'"
                if option == "03" : #작성자
                    sql += "CC.EMP_NAME LIKE '%"+ keyword +"%' OR AA.QNA_WR_NM LIKE '%"+ keyword +"%'"

                sql += "))ORDER BY B.QNA_ORIGIN_NO DESC, B.QNA_SORTS ASC"

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
        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "UPDATE TB_WRK_TM_MGMT_M " \
                      "   SET REST_TM  = '" + restTm + "' " \
                      "   WHERE EMP_EMAL_ADDR = '" + email + "' " \
                      "   AND WRK_DT = '" + dt + "' "
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
        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 쿼리문 실행
                sql = "UPDATE TB_WRK_TM_MGMT_M " \
                      "   SET DINN_REST_TM  = '" + dinnRestTm + "' " \
                      "   WHERE EMP_EMAL_ADDR = '" + email + "' " \
                      "   AND WRK_DT = '" + dt + "' "
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

class popUpData(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        logging.debug('================== App Start ==================')
        logging.debug(data)
        logging.debug('================== App End ==================')

        #requirements pymysql import 후 커넥트 사용
        mysql_con = getMariaConn()
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT  NVL(REST_TM, '0') AS REST_TM "\
                    + "       ,NVL(DINN_REST_TM, '0') AS DINN_REST_TM "\
                    + "  FROM TB_WRK_TM_MGMT_M "\
                    + " WHERE EMP_EMAL_ADDR = '" + data["email"] + "' "\
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

class deptInfo(Resource): # Mariadb 연결 진행
    def get(self):
        data = request.get_json()

        # get data
        #name = data["name"]
        logging.debug('================== App Start ==================')
        logging.debug(data)
        logging.debug(request.args.get('param'))
        logging.debug('================== App End ==================')

        #requirements pymysql import 후 커넥트 사용
        #mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
        #                                charset='utf8', autocommit=False)
        mysql_con = getMariaConn()

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                # 전체 부서 조회
                sql = "SELECT C.CMM_CD AS DEPT_CODE" \
                      "     , C.CMM_CD_NAME AS DEPT_NAME" \
                      "     , C.USE_YN" \
                      "     , IFNULL(C.RMKS, '') AS RMKS" \
                      "     , C.EMP_ID" \
                      "     , (SELECT E.EMP_NAME" \
                      "          FROM TB_EMP_MGMT E" \
                      "         WHERE E.EMP_ID = C.EMP_ID" \
                      "       ) AS EMP_NAME" \
                      "     , IFNULL(C.GM_ID, '') AS GM_ID" \
                      "     , IFNULL((SELECT E.EMP_NAME" \
                      "          FROM TB_EMP_MGMT E" \
                      "         WHERE E.EMP_ID = C.GM_ID" \
                      "       ), '') AS GM_NAME" \
                      "  FROM TB_CMM_CD_DETL C" \
                      " WHERE C.CMM_CD_GRP_ID = 'SLIN_BZDP'" \
                      " ORDER BY C.CMM_CD"

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

class deptMgmtRegSubmit(Resource):
    def post(self):
        logger.info('========app.py deptMgmtRegSubmit=========')
        params = request.get_json()
        logger.info(params)

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        ipt_empId2 = request.form['ipt_empId']
        ipt_empNm2 = request.form['ipt_empNm']
        ipt_deptName = request.form['ipt_deptName']
        sessionId = request.form['sessionId']
        ipt_gmId2 = request.form['ipt_gmId']


        logging.debug("====Param data====")

        logging.debug("ipt_empId2 = " + ipt_empId2)
        logging.debug("ipt_empNm2 = " + ipt_empNm2)
        logging.debug("ipt_deptName = " + ipt_deptName)
        logging.debug("sessionId = " + sessionId)



        logging.debug("=====================")



        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)


        logging.debug("save Start")

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql= "INSERT INTO TB_CMM_CD_DETL(CMM_CD_GRP_ID, CMM_CD, CMM_CD_NAME, USE_YN, REG_DATE, REG_EMP_NO, CHG_DATE, CHG_EMP_NO, EMP_ID, GM_ID) "\
                     "VALUES( "\
                     "        'SLIN_BZDP' "\
                     "      , (SELECT * FROM (SELECT MAX(CMM_CD)+1 FROM TB_CMM_CD_DETL WHERE CMM_CD_GRP_ID = 'SLIN_BZDP' AND CMM_CD <> '99') A) "\
                     "      , '" + ipt_deptName + "' "\
                     "      , 'Y' "\
                     "      , NOW() "\
                     "      , '" + sessionId + "' "\
                     "      , NOW() "\
                     "      , '" + sessionId + "' "\
                     "      , '" + ipt_empId2 + "' "\
                     "      , '" + ipt_gmId2 + "' "\
                     " ) "\

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

class deptMgmtEditSubmit(Resource):
    def post(self):
        logger.info('========app.py empMgmtEditSubmit=========')
        params = request.get_json()
        logger.info(params)

        for row in request.form:
            logger.info(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        ipt_empId = request.form['ipt_empId']
        ipt_empNm = request.form['ipt_empNm']
        ipt_deptCode = request.form['ipt_deptCode']
        ipt_deptName = request.form['ipt_deptName']
        sessionId = request.form['sessionId']
        ipt_gmId = request.form['ipt_gmId']


        logging.debug("====Param data====")

        logging.debug("ipt_empId = " + ipt_empId)
        logging.debug("ipt_empNm = " + ipt_empNm)
        logging.debug("ipt_deptCode = " + ipt_deptCode)
        logging.debug("ipt_deptName = " + ipt_deptName)
        logging.debug("sessionId = " + sessionId)
        logging.debug("ipt_gmId = " + ipt_gmId)

        logging.debug("=====================")



        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8', autocommit=False)


        logging.debug("save Start")

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                # 부서정보 변경
                sql= "UPDATE TB_CMM_CD_DETL "\
                     "   SET CMM_CD_NAME = '" + ipt_deptName + "' "\
                     "     , EMP_ID =  '" + ipt_empId + "' "\
                     "     , GM_ID =  '" + ipt_gmId + "' "\
                     "     , CHG_DATE = NOW() "\
                     "     , CHG_EMP_NO = '" + sessionId + "' "\
                     " WHERE CMM_CD_GRP_ID = 'SLIN_BZDP' "\
                     "   AND CMM_CD = '" + ipt_deptCode + "' "

                logger.info(sql)
                cursor.execute(sql)

                # 부서내 사용자의 현장대리인, 사업부장, 부서명 변경
                sql = "UPDATE TB_EMP_MGMT "\
                      "   SET EMP_PR = '" + ipt_empId + "' "\
                      "     , EMP_GM = '" + ipt_gmId + "' "\
                      "     , DEPT_NAME = '" + ipt_deptName + "' "\
                      " WHERE DEPT_CD = '" + ipt_deptCode + "' "

                logger.info(sql)
                cursor.execute(sql)

                # 변경한 부서의 현장대리인의 권한, 부서코드, 부서명 변경
                sql = "UPDATE TB_EMP_MGMT " \
                      "   SET AUTH_ID = 'PR' " \
                      "     , DEPT_CD = '" + ipt_deptCode + "' "\
                      "     , DEPT_NAME = '" + ipt_deptName + "' "\
                      " WHERE EMP_ID = '" + ipt_empId + "' "
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

class deptOneInfo(Resource): # Mariadb 연결 진행
    def get(self):

        data = request.get_json()

        logging.debug('================== App Start ==================')
        logging.debug(data)
        logging.debug(data["deptCode"])
        logging.debug('================== App End ==================')

        #requirements pymysql import 후 커넥트 사용
        mysql_con = getMariaConn()
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                #쿼리문 실행
                sql = "SELECT C.CMM_CD AS DEPT_CODE" \
                      "     , C.CMM_CD_NAME AS DEPT_NAME" \
                      "     , C.USE_YN" \
                      "     , IFNULL(C.RMKS, '') AS RMKS" \
                      "     , C.EMP_ID" \
                      "     , (SELECT E.EMP_NAME" \
                      "          FROM TB_EMP_MGMT E" \
                      "         WHERE E.EMP_ID = C.EMP_ID" \
                      "       ) AS EMP_NAME" \
                      "     , C.GM_ID" \
                      "     , (SELECT E.EMP_NAME" \
                      "          FROM TB_EMP_MGMT E" \
                      "         WHERE E.EMP_ID = C.GM_ID" \
                      "       ) AS GM_NAME" \
                      "  FROM TB_CMM_CD_DETL C" \
                      " WHERE C.CMM_CD_GRP_ID = 'SLIN_BZDP'" \
                      "   AND C.CMM_CD = '" + data["deptCode"] + "'"\
                      " ORDER BY C.CMM_CD"

                logging.debug(sql)
                cursor.execute(sql)
                logging.debug('getEditDeptInfo SUCCESS')

        finally:
            mysql_con.close()
            logging.debug('getEditDeptInfo CLOSE')



        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return json.dumps(result2, indent=4, cls=DateTimeEncoder)

class diliScheduleTotalMgmt(Resource):
    def get(self):

        logging.debug('diliScheduleTotalMgmt Start')

        # get data
        data = request.get_json()

        mysql_con = pymysql.connect(host=getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT CASE WHEN NVL(B.EMP_EMAL_ADDR, '') = '' THEN A.EMP_EMAL_ADDR" \
                      "            WHEN NVL(A.EMP_EMAL_ADDR, '') = '' THEN B.EMP_EMAL_ADDR" \
                      "                                               ELSE A.EMP_EMAL_ADDR" \
                      "                                                END EMP_EMAL_ADDR" \
                      "      ,(SELECT D.CMM_CD_NAME" \
                      "		     FROM TB_CMM_CD_DETL D" \
                      "		         ,TB_EMP_MGMT E" \
                      "			WHERE D.CMM_CD_GRP_ID = 'SLIN_BZDP'" \
                      "			  AND D.CMM_CD = E.DEPT_CD" \
                      "			  AND E.EMP_EMAIL = NVL(A.EMP_EMAL_ADDR, B.EMP_EMAL_ADDR)) DEPT_NAME" \
                      "	     ,(SELECT C.EMP_NAME " \
                      "	         FROM TB_EMP_MGMT C" \
                      "	        WHERE C.EMP_EMAIL = NVL(A.EMP_EMAL_ADDR, B.EMP_EMAL_ADDR)) OCEM_NAME" \
                      "      ,SUM(" \
                      "            CASE WHEN NVL(B.PTO_KD_CD, 'X') IN ('01', '03') /*01 연차,02 반차,03 기타*/ " \
                      "                 THEN SUBSTRING(B.WRK_TME, 1, 2)" \
                      "                 WHEN NVL(B.PTO_KD_CD, 'X') = '02' /*02 반차*/" \
                      "                 THEN SUBSTRING(DATE_SUB(STR_TO_DATE(NVL(A.ALL_WRK_TM, '000000'), '%H%i%s'), INTERVAL A.REST_TM + A.DINN_REST_TM MINUTE), 1, 2)" \
                      "                 ELSE SUBSTRING(DATE_SUB(DATE_ADD(STR_TO_DATE(NVL(A.ALL_WRK_TM, '000000'), '%H%i%s'), INTERVAL TIME_TO_SEC(STR_TO_DATE(LPAD(NVL(B.WRK_TME, A.NGHT_WRK_TM), 6, '0'), '%H%i%s')) SECOND), INTERVAL A.REST_TM + A.DINN_REST_TM MINUTE), 1, 2)" \
                      "             END" \
                      "          ) ALL_WRK_TM_T" \
                      "      ,SUM(" \
                      "            CASE WHEN NVL(B.PTO_KD_CD, 'X') IN ('01', '03') /*01 연차,02 반차,03 기타*/ " \
                      "                 THEN SUBSTRING(B.WRK_TME, 3, 2)" \
                      "                 WHEN NVL(B.PTO_KD_CD, 'X') = '02' /*02 반차*/" \
                      "                 THEN SUBSTRING(DATE_SUB(STR_TO_DATE(NVL(A.ALL_WRK_TM, '000000'), '%H%i%s'), INTERVAL A.REST_TM + A.DINN_REST_TM MINUTE), 4, 2)" \
                      "                 ELSE SUBSTRING(DATE_SUB(DATE_ADD(STR_TO_DATE(NVL(A.ALL_WRK_TM, '000000'), '%H%i%s'), INTERVAL TIME_TO_SEC(STR_TO_DATE(LPAD(NVL(B.WRK_TME, A.NGHT_WRK_TM), 6, '0'), '%H%i%s')) SECOND), INTERVAL A.REST_TM + A.DINN_REST_TM MINUTE), 4, 2)" \
                      "             END" \
                      "          ) ALL_WRK_TM_M" \
                      "      ,(SUM(CASE WHEN NVL(A.NGHT_WRK_TM, '') != '' AND NVL(A.NGHT_WRK_TM, '') != '000000' THEN SUBSTRING(NVL(A.NGHT_WRK_TM, ''), 1, 2)" \
                      "                                                                                          ELSE ''" \
                      "                                                                                          END )" \
                      "       + FLOOR(SUM(CASE WHEN NVL(A.NGHT_WRK_TM, '') != '' AND NVL(A.NGHT_WRK_TM, '') != '000000' THEN SUBSTRING(NVL(A.NGHT_WRK_TM, ''), 3, 2)" \
                      "                                                                                          ELSE ''" \
                      "                                                                                          END )/60) ) NGHT_WRK_YN_T" \
                      "     ,MOD(SUM(CASE WHEN NVL(A.NGHT_WRK_TM, '') != '' AND NVL(A.NGHT_WRK_TM, '') != '000000' THEN SUBSTRING(NVL(A.NGHT_WRK_TM, ''), 3, 2)" \
                      "                                                                                          ELSE ''" \
                      "                                                                                          END ),60) NGHT_WRK_YN_M" \
                      "     ,(SUM(CASE WHEN NVL(A.HLDY_WRK_TM, '') != '' AND NVL(A.HLDY_WRK_TM, '') != '000000' THEN SUBSTRING(NVL(A.HLDY_WRK_TM, ''), 1, 2)" \
                      "                                                                                          ELSE ''" \
                      "                                                                                          END )" \
                      "       + FLOOR(SUM(CASE WHEN NVL(A.HLDY_WRK_TM, '') != '' AND NVL(A.HLDY_WRK_TM, '') != '000000' THEN SUBSTRING(NVL(A.HLDY_WRK_TM, ''), 3, 2)" \
                      "                                                                                          ELSE ''" \
                      "                                                                                          END )/60) ) HLDY_WRK_YN_T" \
                      "     ,MOD(SUM(CASE WHEN NVL(A.HLDY_WRK_TM, '') != '' AND NVL(A.HLDY_WRK_TM, '') != '000000' THEN SUBSTRING(NVL(A.HLDY_WRK_TM, ''), 3, 2)" \
                      "                                                                                          ELSE ''" \
                      "                                                                                          END ),60) HLDY_WRK_YN_M" \
                      "  FROM TB_WRK_TM_MGMT_M A" \
                      "  LEFT OUTER JOIN" \
                      "       TB_APVL_REQ_MGMT_M B" \
                      "   ON (A.WRK_DT = B.WRK_DT OR A.WRK_DT BETWEEN B.HOLI_TERM1 AND B.HOLI_TERM2) "\
                      "   AND A.EMP_EMAL_ADDR = B.EMP_EMAL_ADDR "\
                      "   AND B.APVL_REQ_DIVS <> '99'" \
                      " WHERE SUBSTRING(A.WRK_DT, 1, 7) = '" + data["wrkDt"] + "'"
                if data["dept"] != "" and data["dept"] != "00":
                    sql += "    AND A.EMP_EMAL_ADDR IN (SELECT H.EMP_EMAIL" \
                           "                              FROM TB_EMP_MGMT H" \
                           "                             WHERE H.DEPT_CD = '" + data["dept"] + "')"
                sql += "GROUP BY EMP_EMAL_ADDR"

                logging.debug(sql + "*****************")
                cursor.execute(sql)
                logging.debug('diliScheduleTotalMgmt SUCCESS')
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

api.add_resource(wrkTimeInfoByEml , '/wrkTimeInfoByEml')      # _
api.add_resource(yryMgmt          , '/yryMgmt')               # _
api.add_resource(hldyMgmt         , '/hldyMgmt')              # _
api.add_resource(wrkApvlReq       , '/wrkApvlReq')            # _
api.add_resource(saveApvlReq      , '/saveApvlReq')           # 근무 결재 요청 저장
api.add_resource(saveApvlAcpt     , '/saveApvlAcpt')          # 근무 결재 승인 저장
api.add_resource(apvlReqHist      , '/apvlReqHist')           # 근무 결재 요청 내역 조회
api.add_resource(duplApvlReqCnt   , '/duplApvlReqCnt')        # 동일 일자 근무 결재 요청 내역 건수 조회
api.add_resource(duplApvlYryReqCnt   , '/duplApvlYryReqCnt')        # 동일 일자 근무 연차 요청 내역 건수 조회
api.add_resource(duplWrkCnt       , '/duplWrkCnt')            # 선결재 동일 일자 스케줄 등록 건수 조회
api.add_resource(wrkTm            , '/wrkTm')                 # 선결재 동일 일자 스케줄 조회(정규 근무 시간정보)
api.add_resource(apvlReqHistDetl  , '/apvlReqHistDetl')       # 연차 결재 요청 상세 조회
api.add_resource(apvlReqWrkHistDetl  , '/apvlReqWrkHistDetl')       # 근무 결재 요청 상세 조회
api.add_resource(apvlAcptHist     , '/apvlAcptHist')          # 근무 결재 승인 내역 조회

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
api.add_resource(empDeptGm,'/empDeptGm')                    #이메일로 사용자 부서 사업부장(GM) 정보 조회
api.add_resource(empDeptPr,'/empDeptPr')                    #이메일로 사용자 부서 현장대리인(PR) 정보 조회
api.add_resource(saveYryApvlReq,'/saveYryApvlReq')          #연차요청등록
api.add_resource(saveYryApvlCncl,'/saveYryApvlCncl')        #연차요청취소
api.add_resource(weekGridData,'/weekGridData') #api 선언
api.add_resource(apvlInfo,'/apvlInfo') #api 선언
api.add_resource(monthGridData,'/monthGridData') #api 선언
api.add_resource(insertStrtTm,'/insertStrtTm') #api 선언
api.add_resource(updateEndTm,'/updateEndTm') #api 선언
api.add_resource(updateWrkTimeConfirm,'/updateWrkTimeConfirm') #api 선언
api.add_resource(insertWrkTimeGen,'/insertWrkTimeGen') #api 선언
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
api.add_resource(popUpData,'/popUpData') #api 선언
api.add_resource(deptInfo,'/deptInfo') #api 선언
api.add_resource(deptMgmtRegSubmit,'/deptMgmtRegSubmit') #api 선언
api.add_resource(deptMgmtEditSubmit,'/deptMgmtEditSubmit') #api 선언
api.add_resource(deptOneInfo,'/deptOneInfo') #api 선언
api.add_resource(diliScheduleTotalMgmt,'/diliScheduleTotalMgmt') #api 선언

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5006, debug=True)