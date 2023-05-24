from flask import Flask, jsonify, request
from flask_restful import Api, Resource

import logging
logging.basicConfig(level=logging.DEBUG)
import bcrypt
import socket

import json
import pymysql
import os

app = Flask(__name__)
api = Api(app)
logger = logging.getLogger(__name__)

##client = MongoClient("mongodb://skil_db:27017")
#db = client.projectDB
#users = db["Users"]

""" 
HELPER FUNCTIONS
"""


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

def getSystemInfo():
    logging.debug('prj Server')
    logging.debug("=====>>>>>>>>>>> " + os.environ['SPRING_PROFILES_ACTIVE'])
    try:
        if (os.environ['SPRING_PROFILES_ACTIVE'] == "prod"):
            logging.debug('Prod Server')
            return "mariadb"
        else :
            logging.debug('Local Server')
            return "112.220.26.195"

    except Exception as e:
        logging.exception(e)

"""
RESOURCES
"""


class Hello(Resource):
    def get(self):
        return "This is Project Management API!"


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
        #data = request.form.get('data')

        return jsonify({'user': data["username"], 'mail':data['email']})


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

class Health(Resource):
    def get(self):
        retJson = {
            "status": "UP"
        }
        return jsonify(retJson)

#프로젝트 정보 수정 시 해당 프로젝트 정보 조회
class retrievePrjInfo(Resource):
    def get(self):
        params = request.get_json()

        logging.debug('retrievePrjInfo Start')
        prj_cd = request.args.get('prj_cd')

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT PRJ_NAME, " \
                             "PRJ_CNCT_CD, " \
                             "GNR_CTRO, " \
                             "CTRO, " \
                             "CNCT_AMT, " \
                             "SLIN_BZDP, " \
                             "JOB_DIVS_CD, " \
                             "PGRS_STUS_CD, " \
                             "CNTC_STRT_DAY, " \
                             "CNTC_END_DAY, " \
                             "RMKS " \
                      "FROM TB_PRJ_INFO " \
                      "WHERE PRJ_CD = %s"
                cursor.execute(sql, prj_cd)
                logging.debug('retrievePrjInfo SUCCESS')
        finally:
            mysql_con.close()

        result = cursor.fetchall()
        logging.debug(result)

        return result

#프로젝트 정보 수정 시 해당 프로젝트 요구 스킬 조회
class retrieveReqSkil(Resource):
    def get(self):
        params = request.get_json()

        logging.debug('retrieveReqSkil Start')
        prj_cd = request.args.get('prj_cd')

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT PRJ_CD, " \
                             "SKIL_DIVS_CD, " \
                             "SKIL_NAME " \
                      "FROM TB_PRJ_REQ_SKIL A " \
                      "WHERE PRJ_CD = %s;"
                cursor.execute(sql, prj_cd)
                logging.debug('retrieveReqSkil SUCCESS')
        finally:
            mysql_con.close()

        result = cursor.fetchall()
        logging.debug(result)

        return result

class devMgmtSearch(Resource):
    def get(self):
        # Get posted data from request
        logging.debug("search start")

        # get data
        devpBlco = request.args.get('devpBlco')
        empName = request.args.get('empName')
        devpDivsCd = request.args.get('devpDivsCd')

        logging.debug('---------------SEARCH---------------')
        logging.debug('devpBlco : ' + devpBlco)
        logging.debug('empName : ' + empName)
        logging.debug('devpDivsCd : ' + devpDivsCd)
        logging.debug('------------------------------------')

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT  A.EMP_NO, " \
                      "        A.EMP_NAME, " \
                      "        A.DEPT_CD AS DEVP_BLCO_CD, " \
                      "        DEPT.CMM_CD_NAME AS DEVP_BLCO, " \
                      "        A.CNTC_DIVS_CD, " \
                      "        CNTC.CMM_CD_NAME AS CNTC_DIVS_NAME, " \
                      "        A.DEVP_GRD_CD, " \
                      "        DEVP.CMM_CD_NAME AS DEVP_GRD_NAME " \
                      "FROM (       SELECT FRLC.EMP_NO AS EMP_NO, " \
                      "                    FRLC.EMP_NAME AS EMP_NAME, " \
                      "                    FRLC.EMP_DEPT_CD AS DEPT_CD, " \
                      "                    FRLC.CNTC_DIVS_CD AS CNTC_DIVS_CD, " \
                      "                    FRLC.DEVP_GRD_CD AS DEVP_GRD_CD " \
                      "              FROM TB_FRLC_DEVP_INFO  FRLC " \
                      "              WHERE FRLC.DEVP_USE_YN ='Y' " \
                      "              GROUP BY FRLC.EMP_NO " \
                      "              UNION ALL " \
                      "              SELECT  EMP.EMP_ID AS EMP_NO, " \
                      "                      EMP.EMP_NAME AS EMP_NAME, " \
                      "                      EMP.DEPT_CD AS DEPT_CD, " \
                      "                      '01' AS CNTC_DIVS_CD, " \
                      "                      EMP.SKIL_GRADE AS DEVP_GRD_CD " \
                      "              FROM TB_EMP_MGMT EMP )A, " \
                      "              TB_CMM_CD_DETL CNTC, " \
                      "              TB_CMM_CD_DETL DEPT, " \
                      "              TB_CMM_CD_DETL DEVP " \
                      "      WHERE 1=1 " \
                      "      AND A.CNTC_DIVS_CD = CNTC.CMM_CD " \
                      "		 AND A.DEPT_CD = DEPT.CMM_CD " \
                      "		 AND A.DEVP_GRD_CD = DEVP.CMM_CD " \
                      "      AND CNTC.CMM_CD_GRP_ID = 'CNTC_DIVS_CD' " \
                      "      AND DEPT.CMM_CD_GRP_ID = 'SLIN_BZDP' " \
                      "      AND DEVP.CMM_CD_GRP_ID = 'DEVP_GRD_CD' "
                if devpBlco != "":
                    sql = sql + "AND A.DEPT_CD = '" + devpBlco + "' "
                if empName != "":
                    sql = sql + "AND A.EMP_NAME LIKE '%" + empName + "%' "
                if devpDivsCd != "":
                    sql = sql + "AND A.CNTC_DIVS_CD = '" + devpDivsCd + "' "
                logging.debug(sql)

                cursor.execute(sql)
        finally:
            mysql_con.close()

        result2 = cursor.fetchall()

        return result2

#공통 코드 조회
class retrieveCmmCd(Resource):
    def get(self):
        params = request.get_json()

        logging.debug('retrieveCmmCd Start')

        grp_id = request.args.get('grp_id')

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT " \
                      "CMM_CD, CMM_CD_NAME " \
                      "FROM TB_CMM_CD_DETL A " \
                      "WHERE CMM_CD_GRP_ID = %s;"
                cursor.execute(sql, grp_id)
                logging.debug('retrieveCmmCd SUCCESS')
        finally:
            mysql_con.close()

        result = cursor.fetchall()
        logging.debug(result)

        return result


#프로젝트 등록 스킬명 조회
class retrieveSkilName(Resource):
    def get(self):
        params = request.get_json()

        logging.debug('retrieveSkilName Start')

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT SKIL_DIVS_CD, " \
                             "SKIL_NAME " \
                      "FROM TB_SKIL_MGNT_CD A "
                cursor.execute(sql)
                logging.debug('retrieveSkilName SUCCESS')
        finally:
            mysql_con.close()

        result = cursor.fetchall()
        logging.debug(result)

        return result

#프로젝트 저장
class prjSave(Resource):
        def post(self):

            params = request.get_json()

            logging.debug("save start")

            for row in request.form:
                logging.debug(row+':'+request.form[row])
                globals()[row] = request.form[row]

            prj_cd = request.form['prj_cd']
            use_yn = 'Y'

            mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8')

            try:
                with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                    # 프로젝트 정보 수정
                    if prj_cd:
                        logging.debug('prj_cd exist')
                        logging.debug(prj_cd)
                    # 프로젝트 최초 등록
                    else:
                        logging.debug('prj_cd is null')
                        # 프로젝트 코드 채번
                        sql = "SELECT CONCAT('PRJ','_',( SELECT LPAD((SELECT NVL(SUBSTR(MAX(PRJ_CD), 5)+1, 1) " \
                              "FROM TB_PRJ_INFO),6,'0'))) AS PRJ_CD"
                        cursor.execute(sql)
                        prjResult = cursor.fetchone()
                        prj_cd = prjResult['PRJ_CD']

                    sql = "INSERT INTO TB_PRJ_INFO(`PRJ_CD`, " \
                                                  "`PRJ_NAME`, " \
                                                  "`PRJ_CNCT_CD`, " \
                                                  "`GNR_CTRO`, " \
                                                  "`CTRO`, " \
                                                  "`CNCT_AMT`, " \
                                                  "`SLIN_BZDP`, " \
                                                  "`JOB_DIVS_CD`, " \
                                                  "`PGRS_STUS_CD`, " \
                                                  "`CNTC_STRT_DAY`, " \
                                                  "`CNTC_END_DAY`, " \
                                                  "`REG_EMP_NO`, " \
                                                  "`REG_DATE`, " \
                                                  "`CHG_EMP_NO`, " \
                                                  "`CHG_DATE`, " \
                                                  "`RMKS`, " \
                                                  "`USE_YN`) " \
                          "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, NOW(), %s, %s)" \
                          "ON DUPLICATE KEY UPDATE " \
                                                  "PRJ_NAME = %s, " \
                                                  "PRJ_CNCT_CD = %s, " \
                                                  "GNR_CTRO = %s, " \
                                                  "CTRO = %s, " \
                                                  "CNCT_AMT = %s, " \
                                                  "SLIN_BZDP = %s, " \
                                                  "JOB_DIVS_CD = %s, " \
                                                  "PGRS_STUS_CD = %s, " \
                                                  "CNTC_STRT_DAY = %s, " \
                                                  "CNTC_END_DAY = %s, " \
                                                  "CHG_EMP_NO = %s, " \
                                                  "CHG_DATE = NOW(), " \
                                                  "RMKS = %s"
                    cursor.execute(sql, (
                        prj_cd, prj_name, prj_cnct_cd, gnr_ctro, ctro, cnct_amt, slin_bzdp, job_divs, pgrs_stus, cntc_strt_day, cntc_end_day, userId, userId, rmks, use_yn,
                        prj_name, prj_cnct_cd, gnr_ctro, ctro, cnct_amt, slin_bzdp, job_divs, pgrs_stus, cntc_strt_day, cntc_end_day, userId, rmks))
                    mysql_con.commit()
                    logging.debug('PRJ_INFO SUCCESS')

                    # 프로젝트 수정 시 요구 스킬 삭제 후 업데이트
                    sql = "DELETE FROM TB_PRJ_REQ_SKIL " \
                          "WHERE PRJ_CD = %s"
                    cursor.execute(sql, prj_cd)
                    mysql_con.commit()
                    logging.debug('REQ_SKIL DELETE SUCCESS')

                    for i in range(1, int(trCount)+1):
                        req_skil_divs = request.form['req_skil_divs'+str(i)]
                        logging.debug('req_skil_divs : ' + req_skil_divs)
                        if req_skil_divs != '00':
                            req_skil_name = request.form['req_skil_name'+str(i)]
                            logging.debug('req_skil_name : ' + req_skil_name)

                            sql1 = "SELECT IFNULL(MAX(PRJ_REQ_SKIL_NO) + 1, 1) AS PRJ_REQ_SKIL_NO FROM TB_PRJ_REQ_SKIL WHERE PRJ_CD = %s"
                            cursor.execute(sql1, prj_cd)
                            result = cursor.fetchone()
                            prj_req_skil_no = result['PRJ_REQ_SKIL_NO']

                            sql2 = "INSERT INTO TB_PRJ_REQ_SKIL(`PRJ_CD`," \
                                                              "`PRJ_REQ_SKIL_NO`, " \
                                                              "`SKIL_DIVS_CD`, " \
                                                              "`SKIL_NAME`, " \
                                                              "`REG_EMP_NO`, " \
                                                              "`REG_DATE`," \
                                                              " `CHG_EMP_NO`, " \
                                                              "`CHG_DATE`) " \
                                      "VALUES (%s, %s, %s, %s, %s, NOW(), %s, NOW())"
                            cursor.execute(sql2, (prj_cd, prj_req_skil_no, req_skil_divs, req_skil_name, userId, userId))
                            mysql_con.commit()
                            logging.debug('REQ_SKIL'+str(i)+' SUCCESS')
            finally:
                mysql_con.close()

            return prj_cd

#프로젝트 정보 삭제
class prjDelete(Resource):
        def post(self):

            params = request.get_json()

            logging.debug("delete start")
            prj_cd = request.form['prj_cd']

            mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2',
                                            password='1234',
                                            charset='utf8')

            try:
                with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                    sql = "UPDATE TB_PRJ_INFO SET USE_YN = 'N' " \
                          "WHERE PRJ_CD = %s"
                    cursor.execute(sql, prj_cd)
                    mysql_con.commit()
                    logging.debug('PRJ_INFO SUCCESS')

                    sql = "DELETE FROM TB_PRJ_REQ_SKIL " \
                          "WHERE PRJ_CD = %s"
                    cursor.execute(sql, prj_cd)
                    mysql_con.commit()
                    logging.debug('REQ_SKIL DELETE SUCCESS')
            finally:
                mysql_con.close()

            retJson = {
                "status": 200,
                "msg": "Data has been saved successfully"
            }

            return jsonify(retJson)

#프리 개발자 정보 수정 시 해당 개발자 정보 조회
class retrievePrjDetlInfo(Resource):
    def get(self):
        params = request.get_json()

        logging.debug('retrievePrjDetlInfo Start')
        prjCd = request.args.get('prjCd')

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT PRJ.PRJ_CD, " \
                      "PRJ.PRJ_NAME," \
                      "PRJ_CNCT_CD," \
                      "JOBDIV.CMM_CD_NAME AS JOB_DIVS_NM," \
                      "CONCAT(PRJ.CNTC_STRT_DAY,' ~ ',PRJ.CNTC_END_DAY) AS CNTC_TERM " \
                      "FROM TB_PRJ_INFO PRJ, " \
                      "TB_CMM_CD_DETL JOBDIV " \
                      "WHERE PRJ.JOB_DIVS_CD = JOBDIV.CMM_CD " \
                      "AND JOBDIV.CMM_CD_GRP_ID ='JOB_DIVS_CD' " \
                      "AND PRJ.PRJ_CD = %s"
                cursor.execute(sql, prjCd)
                logging.debug('retrievePrjDetlInfo SUCCESS')
        finally:
            mysql_con.close()

        result1 = cursor.fetchall()
        logging.debug(result1)

        return result1

# 프로젝트별투입현황관리 조회
class prjInpuSearch(Resource):
    def get(self):
        # Get posted data from request
        logging.debug("search start")

        # get data
        prjCd = request.args.get('prjCd')

        logging.debug('---------------SEARCH---------------')
        logging.debug('prjCd : ' + prjCd)
        logging.debug('------------------------------------')

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:

                sql = "SELECT PSTAR.PRJ_CD," \
                              "PSTAR.EMP_NO," \
                              "FRLC.EMP_NAME," \
                              "DEPT.CMM_CD_NAME AS DEPT_NM," \
                              "DEVP.CMM_CD_NAME AS SKIL_GRD," \
                              "CNTC.CMM_CD_NAME AS CNTC_DIVS_NM," \
                              "PSTAR.SLIN_GRD,PSTAR.INPU_STRT_DAY," \
                              "PSTAR.INPU_END_DAY," \
                              "PSTAR.CNTC_STRT_DAY," \
                              "PSTAR.CNTC_END_DAY," \
                              "PSTAR.CRGE_JOB,PSTAR.RMKS " \
                      "FROM TB_PRJ_INPU_STAT_MGMT PSTAR," \
                            "TB_FRLC_DEVP_INFO FRLC," \
                            "TB_CMM_CD_DETL DEPT," \
                            "TB_CMM_CD_DETL DEVP," \
                            "TB_CMM_CD_DETL CNTC " \
                      "WHERE PSTAR.EMP_NO = FRLC.EMP_NO " \
                          "AND FRLC.EMP_DEPT_CD = DEPT.CMM_CD " \
                          "AND FRLC.DEVP_GRD_CD = DEVP.CMM_CD " \
                          "AND FRLC.CNTC_DIVS_CD = CNTC.CMM_CD " \
                          "AND DEPT.CMM_CD_GRP_ID ='SLIN_BZDP' " \
                          "AND DEVP.CMM_CD_GRP_ID ='DEVP_GRD_CD' " \
                          "AND CNTC.CMM_CD_GRP_ID ='CNTC_DIVS_CD' " \
                          "AND PRJ_CD=%s " \
                      "UNION " \
                      "SELECT PSTAR.PRJ_CD, " \
                              "PSTAR.EMP_NO," \
                              "EMP.EMP_NAME,  " \
                              "DEPT.CMM_CD_NAME AS DEPT_NM, " \
                              "DEVP.CMM_CD_NAME AS SKIL_GRD," \
                              "'정규직' AS CNTC_DIVS_CD," \
                              "PSTAR.SLIN_GRD," \
                              "PSTAR.INPU_STRT_DAY," \
                              "PSTAR.INPU_END_DAY," \
                              "PSTAR.CNTC_STRT_DAY," \
                              "PSTAR.CNTC_END_DAY," \
                              "PSTAR.CRGE_JOB, " \
                              "PSTAR.RMKS FROM TB_PRJ_INPU_STAT_MGMT PSTAR," \
                              "TB_EMP_MGMT EMP," \
                              "TB_CMM_CD_DETL DEPT," \
                              "TB_CMM_CD_DETL DEVP " \
                      "WHERE PSTAR.EMP_NO = EMP.EMP_ID " \
                           "AND EMP.DEPT_CD = DEPT.CMM_CD " \
                          "AND EMP.SKIL_GRADE = DEVP.CMM_CD " \
                          "AND DEPT.CMM_CD_GRP_ID ='SLIN_BZDP' " \
                          "AND DEVP.CMM_CD_GRP_ID ='DEVP_GRD_CD' " \
                          "AND PRJ_CD=%s"
                cursor.execute(sql, (prjCd,prjCd))
        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        return result2

# 프로젝트별투입현황관리 삭제
class prjInpuDelete(Resource):

    def post(self):
        # Get posted data from request

        # get data
        prjCd = request.form["prjCd"]
        empNo = request.form["empNo"]

        logging.debug('---------------SEARCH---------------')
        logging.debug('prjCd : ' + prjCd)
        logging.debug('empNo : ' + empNo)
        logging.debug('------------------------------------')

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "DELETE FROM TB_PRJ_INPU_STAT_MGMT WHERE EMP_NO= %s AND PRJ_CD = %s"
                cursor.execute(sql, (empNo, prjCd))
                mysql_con.commit()
        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        return result2

# 프로젝트별투입현황관리 저장
class prjInpuSave(Resource):
    def post(self):
        params = request.get_json()

        logging.debug("save start")
        empNo = request.form['empNo']
        prjCd = request.form['prjCd']
        slinGrd = request.form['slinGrd']
        inpuStrtDay = request.form['inpuStrtDay']
        inpuEndDay = request.form['inpuEndDay']
        cntcStrtDay = request.form['cntcStrtDay']
        cntcEndDay = request.form['cntcEndDay']
        crgeJob = request.form['crgeJob']
        rmks = request.form['rmks']
        state = request.form['state']
        userId = request.form['userId']

        logging.debug('================== App Start ==================')
        logging.debug(params)
        logging.debug('================== App End ==================')

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:

                if state =="created" :
                    logging.debug('[skil_app] app.py : created')
                    sql = "INSERT INTO TB_PRJ_INPU_STAT_MGMT(EMP_NO, PRJ_CD, SLIN_GRD, INPU_STRT_DAY, INPU_END_DAY, CNTC_STRT_DAY, CNTC_END_DAY, CRGE_JOB, RMKS, REG_EMP_NO, REG_DATE) " \
                          "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,NOW())"
                    cursor.execute(sql, (empNo, prjCd, slinGrd, inpuStrtDay, inpuEndDay, cntcStrtDay, cntcEndDay, crgeJob, rmks, userId))
                    mysql_con.commit()
                else:
                    logging.debug('[skil_app] app.py : modified')
                    sql = "UPDATE TB_PRJ_INPU_STAT_MGMT " \
                          "SET SLIN_GRD=%s, INPU_STRT_DAY=%s, INPU_END_DAY=%s,  CNTC_STRT_DAY=%s, CNTC_END_DAY=%s, CRGE_JOB=%s, RMKS=%s, CHG_EMP_NO=%s, CHG_DATE= NOW()" \
                          "WHERE EMP_NO = %s AND PRJ_CD = %s "
                    cursor.execute(sql, (slinGrd, inpuStrtDay, inpuEndDay, cntcStrtDay, cntcEndDay, crgeJob, rmks, userId , empNo, prjCd))
                    mysql_con.commit()
        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been saved successfully"
        }

        return jsonify(retJson)

class prjListSearch(Resource):
    def get(self):
        # Get posted data from request
        logging.debug("prjListSearch start")

        # get data
        deptDiv = request.args.get('deptDiv')
        skilDiv = request.args.get('skilDiv')
        logging.debug('---------------SEARCH---------------')
        logging.debug('deptDiv : ' + deptDiv)
        logging.debug('skilDiv : ' + skilDiv)
        logging.debug('------------------------------------')

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT PRJ_CD, PRJ_NAME, GROUP_CONCAT(C.SKIL_NAME) AS SKIL_NAME, GNR_CTRO, CTRO, PRJ_CNCT_CD, SLIN_BZDP, JOB_DIVS_CD, CNTC_STRT_DAY" \
                      ", CNTC_END_DAY, PGRS_STUS_CD, RMKS " \
                      "FROM (SELECT A.PRJ_CD, PRJ_NAME, B.SKIL_NAME, GNR_CTRO, CTRO,PRJ_CNCT_CD" \
                        ", (SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL WHERE CMM_CD_GRP_ID = 'SLIN_BZDP' AND A.SLIN_BZDP = CMM_CD) AS SLIN_BZDP" \
                        ", (SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL WHERE CMM_CD_GRP_ID = 'JOB_DIVS_CD' AND A.JOB_DIVS_CD = CMM_CD) AS JOB_DIVS_CD" \
                        ", CNTC_STRT_DAY, CNTC_END_DAY" \
                        ", (SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL WHERE CMM_CD_GRP_ID = 'PGRS_STUS_CD' AND A.PGRS_STUS_CD = CMM_CD) AS PGRS_STUS_CD" \
                        ", RMKS " \
                        "FROM TB_PRJ_INFO A " \
                        "LEFT JOIN TB_PRJ_REQ_SKIL B " \
                        "ON A.PRJ_CD = B.PRJ_CD " \
                        "WHERE 1=1 " \
                        "AND USE_YN = 'Y'"
                sql2 = ") C GROUP BY PRJ_CD"
                if deptDiv == "" and skilDiv == "":
                    logging.debug('##### sql : ' + sql + sql2)
                    cursor.execute(sql + sql2)
                else:
                    if deptDiv != "" and skilDiv != "":
                        sql += "AND SLIN_BZDP = %s" \
                               "AND SKIL_DIVS_CD = %s"
                        logging.debug('##### sql : ' + sql + sql2)
                        cursor.execute(sql + sql2, (deptDiv, skilDiv))
                    elif deptDiv != "":
                        sql += "AND SLIN_BZDP = %s"
                        logging.debug('##### sql : ' + sql + sql2)
                        cursor.execute(sql + sql2, deptDiv)
                    else:
                        sql += "AND SKIL_DIVS_CD = %s"
                        logging.debug('##### sql : ' + sql + sql2)
                        cursor.execute(sql + sql2, skilDiv)
        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return result2

#부서 코드 조회
class getDeptCd(Resource):
    def get(self):
        # Get posted data from request
        logging.debug("getDeptCd Start")

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT CMM_CD, CMM_CD_NAME FROM TB_CMM_CD_DETL WHERE CMM_CD_GRP_ID = 'SLIN_BZDP'"

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

        return result2

#프리 개발자 정보 수정 시 해당 개발자 정보 조회
class retrieveDevInfo(Resource):
    def get(self):
        params = request.get_json()

        logging.debug('retrieveDevInfo Start')
        emp_no = request.args.get('emp_no')

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT EMP_NAME, " \
                             "EMP_DEPT_CD, " \
                             "EMP_RANK_CD, " \
                             "DEVP_GRD_CD, " \
                             "DEVP_TEL_NO, " \
                             "CNTC_DIVS_CD, " \
                             "DEVP_BLCO, " \
                             "DEVP_BDAY, " \
                             "RMKS " \
                      "FROM TB_FRLC_DEVP_INFO " \
                      "WHERE EMP_NO = %s"
                cursor.execute(sql, emp_no)
                logging.debug('retrieveDevInfo SUCCESS')
        finally:
            mysql_con.close()

        result1 = cursor.fetchall()
        logging.debug(result1)

        return result1

#프리 개발자 정보 저장
class devSave(Resource):
    def post(self):
        params = request.get_json()

        logging.debug("save Start")

        for row in request.form:
            logging.debug(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        emp_no = request.form['emp_no']
        tel_no = request.form['tel_no1'] + '-' + request.form['tel_no2'] + '-' + request.form['tel_no3']
        use_yn = 'Y'

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                if emp_no: #개발자 정보 수정
                    logging.debug('emp_no exist')
                    logging.debug(emp_no)
                else: #개발자 정보 최초 등록
                    logging.debug('emp_no is null')
                    #개발자 사번 채번
                    sql = "SELECT CONCAT('F','_',( SELECT LPAD((SELECT NVL(SUBSTR(MAX(EMP_NO), 3)+1, 1) " \
                          "FROM TB_FRLC_DEVP_INFO),6,'0'))) AS EMP_NO"
                    cursor.execute(sql)
                    empResult = cursor.fetchone()
                    emp_no = empResult['EMP_NO']
                    logging.debug(emp_no)

                sql = "INSERT INTO TB_FRLC_DEVP_INFO (`EMP_NO`, " \
                                                     "`EMP_NAME`, " \
                                                     "`EMP_DEPT_CD`, " \
                                                     "`EMP_RANK_CD`, " \
                                                     "`DEVP_GRD_CD`, " \
                                                     "`DEVP_TEL_NO`, " \
                                                     "`CNTC_DIVS_CD`, " \
                                                     "`DEVP_BLCO`, " \
                                                     "`DEVP_BDAY`, " \
                                                     "`REG_EMP_NO`, " \
                                                     "`REG_DATE`, " \
                                                     "`CHG_EMP_NO`, " \
                                                     "`CHG_DATE`, " \
                                                     "`RMKS`, " \
                                                     "`DEVP_USE_YN`)  " \
                      "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, NOW(), %s, %s)" \
                      "ON DUPLICATE KEY UPDATE " \
                                      "EMP_NAME = %s, " \
                                      "EMP_DEPT_CD = %s, " \
                                      "EMP_RANK_CD = %s, " \
                                      "DEVP_GRD_CD = %s, " \
                                      "DEVP_TEL_NO = %s, " \
                                      "CNTC_DIVS_CD = %s, " \
                                      "DEVP_BLCO = %s, " \
                                      "DEVP_BDAY = %s, " \
                                      "CHG_EMP_NO = %s, " \
                                      "CHG_DATE = NOW(), " \
                                      "RMKS = %s"

                cursor.execute(sql, (emp_no, emp_name, emp_dept, emp_rank, devp_grd, tel_no, cntc_divs, devp_blco, devp_bday, userId, userId, rmks, use_yn
                                     , emp_name, emp_dept, emp_rank, devp_grd, tel_no, cntc_divs, devp_blco, devp_bday, userId, rmks))
                mysql_con.commit()

        finally:
            mysql_con.close()

        # retJson = {
        #     "status": 200,
        #     "msg": "Data has been saved successfully"
        # }
        #
        # return jsonify(retJson)

        return emp_no

#프리 개발자 정보 삭제
class devDelete(Resource):
    def post(self):
        params = request.get_json()

        logging.debug("delete Start")

        emp_name = request.form['emp_name']
        devp_bday = request.form['devp_bday']

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "UPDATE TB_FRLC_DEVP_INFO SET DEVP_USE_YN = 'N' " \
                      "WHERE 1=1 " \
                      "AND EMP_NAME = %s " \
                      "AND DEVP_BDAY = %s"
                cursor.execute(sql, (emp_name, devp_bday))
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
api.add_resource(Health, '/health')

# 프로젝트 등록
api.add_resource(retrievePrjInfo, '/retrievePrjInfo')
api.add_resource(retrieveReqSkil, '/retrieveReqSkil')
api.add_resource(retrieveSkilName, '/retrieveSkilName')
api.add_resource(prjSave, '/prjSave')
api.add_resource(prjDelete, '/prjDelete')

# 프로젝트 투입 관리
api.add_resource(retrievePrjDetlInfo, '/retrievePrjDetlInfo')
api.add_resource(prjInpuSearch, '/prjInpuSearch')
api.add_resource(prjInpuDelete, '/prjInpuDelete')
api.add_resource(prjInpuSave, '/prjInpuSave')

# 프로젝트 목록 조회
api.add_resource(prjListSearch, '/prjListSearch')
api.add_resource(getDeptCd, '/getDeptCd')

# 개발자 조회
api.add_resource(devMgmtSearch, '/devMgmtSearch')

#공통 코드 조회
api.add_resource(retrieveCmmCd, '/retrieveCmmCd')

# 프리 개발자 등록
api.add_resource(retrieveDevInfo, '/retrieveDevInfo')
api.add_resource(devSave, '/devSave')
api.add_resource(devDelete, '/devDelete')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)