from flask import Flask, jsonify, request
from flask_restful import Api, Resource

import logging
logging.basicConfig(level=logging.DEBUG)
import bcrypt
import socket

import json
import pymysql

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
    try:
        if (socket.gethostbyname(socket.gethostname()) == "172.20.0.6" ) :
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
                            sql = "INSERT INTO TB_PRJ_REQ_SKIL(`PRJ_CD`, " \
                                                              "`SKIL_DIVS_CD`, " \
                                                              "`SKIL_NAME`, " \
                                                              "`REG_EMP_NO`, " \
                                                              "`REG_DATE`," \
                                                              " `CHG_EMP_NO`, " \
                                                              "`CHG_DATE`) " \
                                      "VALUES ((SELECT PRJ_CD " \
                                              "FROM TB_PRJ_INFO A " \
                                              "WHERE PRJ_NAME = %s)," \
                                              " %s, %s, %s, NOW(), %s, NOW())"
                            cursor.execute(sql, (prj_name, req_skil_divs, req_skil_name, userId, userId))
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

        mysql_con = pymysql.connect(host='218.151.225.142', port=3306, db='IFG_IMS', user='ims2', password='1234',
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

        mysql_con = pymysql.connect(host='218.151.225.142', port=3306, db='IFG_IMS', user='ims2', password='1234',
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
        #empNo = request.form["empNo"]

        logging.debug('---------------SEARCH---------------')
        logging.debug('prjCd : ' + prjCd)
        #logging.debug('empNo : ' + empNo)
        logging.debug('------------------------------------')

        mysql_con = pymysql.connect(host='218.151.225.142', port=3306, db='IFG_IMS', user='ims2', password='1234',
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

        logging.debug('================== App Start ==================')
        logging.debug(params)
        logging.debug('================== App End ==================')

        mysql_con = pymysql.connect(host='218.151.225.142', port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:

                if state =="created" :
                    logging.debug('[skil_app] app.py : created')
                    sql = "INSERT INTO TB_PRJ_INPU_STAT_MGMT(EMP_NO, PRJ_CD, SLIN_GRD, INPU_STRT_DAY, INPU_END_DAY, CNTC_STRT_DAY, CNTC_END_DAY, CRGE_JOB, RMKS, REG_EMP_NO, REG_DATE) " \
                          "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,NOW())"
                    cursor.execute(sql, (empNo, prjCd, slinGrd, inpuStrtDay, inpuEndDay, cntcStrtDay, cntcEndDay, crgeJob, rmks,'admin'))
                    mysql_con.commit()
                else:
                    logging.debug('[skil_app] app.py : modified')
                    sql = "UPDATE TB_PRJ_INPU_STAT_MGMT " \
                          "SET SLIN_GRD=%s, INPU_STRT_DAY=%s, INPU_END_DAY=%s,  CNTC_STRT_DAY=%s, CNTC_END_DAY=%s, CRGE_JOB=%s, RMKS=%s, CHG_EMP_NO=%s, CHG_DATE= NOW()" \
                          "WHERE EMP_NO = %s AND PRJ_CD = %s "
                    cursor.execute(sql, (slinGrd, inpuStrtDay, inpuEndDay, cntcStrtDay, cntcEndDay, crgeJob, rmks,'admin', empNo, prjCd))
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
        logging.debug("search start")

        # get data
        skilDiv = request.args.get('skilDiv')

        logging.debug('---------------SEARCH---------------')
        logging.debug('skilDiv : ' + skilDiv)
        logging.debug('------------------------------------')

        mysql_con = pymysql.connect(host='218.151.225.142', port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT PRJ_NAME FROM TB_PRJ_INFO"
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)