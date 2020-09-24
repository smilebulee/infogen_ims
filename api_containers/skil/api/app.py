from flask import Flask, jsonify, request
from flask_restful import Api, Resource

import logging
logging.basicConfig(level=logging.DEBUG)
import bcrypt

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
    # if users.find({"Username": username}).count() == 0:
    #     return False
    # else:
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
        mysql_con = pymysql.connect(host='218.151.225.142', port=9876, db='testdb', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM SKIL_TEST "
                cursor.execute(sql)

        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로
        return "This is Skill Management API!"


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

class mariaClass(Resource):
    def get(self):
        mysql_con = pymysql.connect(host='218.151.225.142', port=9876, db='testdb', user='ims2', password='1234',
                                        charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM SKIL_TEST "
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

class devSave(Resource):
    def post(self):
        params = request.get_json()

        logging.debug("save start")
        emp_no = request.form['emp_no']
        name = request.form['name']
        rank = request.form['rank']
        grd = request.form['grd']
        tlno = request.form['tlno1'] + request.form['tlno2'] + request.form['tlno3']
        divs = request.form['divs']
        blco = request.form['blco']
        bday = request.form['bday']
        rmks = request.form['rmks']
        use_yn = 'Y'

        logging.debug('--------------------------------------')
        logging.debug(name)
        logging.debug(rank)
        logging.debug('--------------------------------------')

        logging.debug('================== App Start ==================')
        logging.debug(params)
        logging.debug('================== App End ==================')

        mysql_con = pymysql.connect(host='218.151.225.142', port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:

                if emp_no:
                    logging.debug('emp_no exist')
                    logging.debug(emp_no)

                else:
                    logging.debug('emp_no is null')
                    logging.debug(emp_no)
                    sql = "SELECT CONCAT('F','_',( SELECT LPAD((SELECT NVL(SUBSTR(MAX(EMP_NO), 3)+1, 1) " \
                          "FROM TB_FRLC_DEVP_INFO),6,'0'))) AS EMP_NO"
                    cursor.execute(sql)
                    empResult = cursor.fetchone()
                    emp_no = empResult['EMP_NO']
                    logging.debug(emp_no)

                sql = "INSERT INTO TB_FRLC_DEVP_INFO (`EMP_NO`, " \
                      "`EMP_NAME`, `EMP_RANK_CD`, `DEVP_GRD_CD`, `DEVP_TEL_NO`, `CNTC_DIVS_CD`, " \
                      "`DEVP_BLCO`, `DEVP_BDAY`, `REG_EMP_NO`, `REG_DATE`, `CHG_EMP_NO`, `CHG_DATE`, `RMKS`, `DEVP_USE_YN`)  " \
                      "VALUES(%s," \
                      "%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, NOW(), %s, %s)" \
                      "ON DUPLICATE KEY UPDATE " \
                      "EMP_NAME = %s, EMP_RANK_CD = %s, DEVP_GRD_CD = %s, DEVP_TEL_NO = %s, CNTC_DIVS_CD = %s, DEVP_BLCO = %s, " \
                      "DEVP_BDAY = %s, CHG_EMP_NO = %s, CHG_DATE = NOW(), RMKS = %s"

                cursor.execute(sql, (emp_no, name, rank, grd, tlno, divs, blco, bday, 'admin', 'admin', rmks, use_yn
                                     , name, rank, grd, tlno, divs, blco, bday, 'admin', rmks))
                mysql_con.commit()

        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been saved successfully"
        }

        return jsonify(retJson)


class devDelete(Resource):
    def post(self):

        params = request.get_json()

        logging.debug("delete start")

        name = request.form['name']
        bday = request.form['bday']

        logging.debug('================== SQL START ==================')

        mysql_con = pymysql.connect(host='218.151.225.142', port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "UPDATE TB_FRLC_DEVP_INFO SET DEVP_USE_YN = 'N' " \
                      "WHERE 1=1 " \
                      "AND EMP_NAME = %s " \
                      "AND DEVP_BDAY = %s"
                cursor.execute(sql, (name, bday))
                mysql_con.commit()

        finally:
            mysql_con.close()


        retJson = {
            "status": 200,
            "msg": "Data has been saved successfully"
        }

        return jsonify(retJson)

class prjSave(Resource):
        def post(self):

            params = request.get_json()

            logging.debug("save start")
            logging.debug(request.form)

            for row in request.form:
                logging.debug(row+':'+request.form[row])
                globals()[row] = request.form[row]

            prj_cd = request.form['prj_cd']
            # prj_nm = request.form['prj_nm']
            # cnct_cd = request.form['cnct_cd']
            # gnr_ctro = request.form['gnr_ctro']
            # ctro = request.form['ctro']
            # cnct_amt = request.form['cnct_amt']
            # slin_bzdp = request.form['slin_bzdp']
            # job_divs = request.form['job_divs']
            # pgrs_stus = request.form['pgrs_stus']
            # req_skil_divs1 = request.form['req_skil_divs1']
            # req_skil_name1 = request.form['req_skil_name1']
            # rmks = request.form['rmks']
            use_yn = 'Y'

            logging.debug('--------------------------------------')
            logging.debug(prj_cd + prj_nm + cnct_cd + gnr_ctro + ctro + cnct_amt + slin_bzdp + job_divs + pgrs_stus)
            logging.debug('--------------------------------------')


            mysql_con = pymysql.connect(host='218.151.225.142', port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8')

            try:
                with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:

                    if prj_cd:
                        logging.debug('prj_cd exist')
                        logging.debug(prj_cd)

                    else:
                        logging.debug('prj_cd is null')
                        sql = "SELECT CONCAT('PRJ','_',( SELECT LPAD((SELECT NVL(SUBSTR(MAX(PRJ_CD), 5)+1, 1) " \
                              "FROM TB_PRJ_INFO),6,'0'))) AS PRJ_CD"
                        cursor.execute(sql)
                        prjResult = cursor.fetchone()
                        prj_cd = prjResult['PRJ_CD']

                    sql = "INSERT INTO TB_PRJ_INFO(`PRJ_CD`, `PRJ_NAME`, `PRJ_CNCT_CD`, `GNR_CTRO`, `CTRO`, `CNCT_AMT`," \
                          " `SLIN_BZDP`, `JOB_DIVS_CD`, `PGRS_STUS_CD`, `REG_EMP_NO`, `REG_DATE`, `CHG_EMP_NO`," \
                          " `CHG_DATE`, `RMKS`, `USE_YN`) " \
                          "VALUES(%s, " \
                          "%s, %s, %s, %s, %s, %s, %s, %s, 'admin', NOW(), 'admin', NOW(), %s, %s)" \
                          "ON DUPLICATE KEY UPDATE " \
                          "PRJ_NAME = %s, PRJ_CNCT_CD = %s, GNR_CTRO = %s, CTRO = %s, CNCT_AMT = %s, SLIN_BZDP = %s, " \
                          "JOB_DIVS_CD = %s, PGRS_STUS_CD = %s, CHG_EMP_NO = 'admin', CHG_DATE = NOW(), RMKS = %s"
                    cursor.execute(sql, (
                        prj_cd, prj_nm, cnct_cd, gnr_ctro, ctro, cnct_amt, slin_bzdp, job_divs, pgrs_stus, rmks, use_yn,
                        prj_nm, cnct_cd, gnr_ctro, ctro, cnct_amt, slin_bzdp, job_divs, pgrs_stus, rmks))
                    mysql_con.commit()

                    logging.debug('PRJ_INFO SUCCESS')

                    if not req_skil_divs1 and not "00":

                        sql = "INSERT INTO TB_PRJ_REQ_SKIL(`PRJ_CD`, `SKIL_DIVS`, `SKIL_NAME`, `REG_EMP_NO`, `REG_DATE`," \
                              " `CHG_EMP_NO`, `CHG_DATE`) " \
                              "VALUES ((SELECT PRJ_CD FROM TB_PRJ_INFO A WHERE PRJ_NAME = %s)," \
                              " %s, %s, 'admin', NOW(), 'admin', NOW())"
                        cursor.execute(sql, (prj_nm, req_skil_divs1, req_skil_name1))
                        mysql_con.commit()
                        logging.debug('REQ_SKIL SUCCESS')

            finally:
                mysql_con.close()

            retJson = {
                "status": 200,
                "msg": "Data has been saved successfully"
            }

            return jsonify(retJson)

class prjDelete(Resource):
        def post(self):

            params = request.get_json()

            logging.debug("delete start")

            prj_nm = request.form['prj_nm']

            logging.debug('--------------------------------------')
            logging.debug(prj_nm)
            logging.debug('--------------------------------------')

            logging.debug('================== SQL Start ==================')

            mysql_con = pymysql.connect(host='218.151.225.142', port=3306, db='IFG_IMS', user='ims2',
                                            password='1234',
                                            charset='utf8')

            try:
                with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                    sql = "UPDATE TB_PRJ_INFO SET USE_YN = 'N' " \
                              "WHERE PRJ_NM = %s"
                    cursor.execute(sql, (prj_nm))
                    mysql_con.commit()

                    logging.debug('PRJ_INFO SUCCESS')


            finally:
                mysql_con.close()

            retJson = {
                "status": 200,
                "msg": "Data has been saved successfully"
            }

            return jsonify(retJson)


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
                if prjCd is None or prjCd == "":
                    sql = "SELECT PRJ_CD, EMP_NO,DIVS, SLIN_GRD, INPU_STRT_DAY, INPU_END_DAY, CNTC_STRT_DAY, CNTC_END_DAY, CRGE_JOB, RMKS FROM TB_PRJ_INPU_STAT_MGMT "
                    cursor.execute(sql)
                else:
                    logging.debug("is not null")
                    sql = "SELECT PRJ_CD, EMP_NO,DIVS, SLIN_GRD, INPU_STRT_DAY, INPU_END_DAY, CNTC_STRT_DAY, CNTC_END_DAY, CRGE_JOB, RMKS FROM TB_PRJ_INPU_STAT_MGMT WHERE PRJ_CD=%s"
                    cursor.execute(sql, (prjCd))
        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        return result2


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

class skilMgmtSearch(Resource):
    def get(self):
        # Get posted data from request
        logging.debug("search start")

        # get data
        dept = request.args.get('dept')
        name = request.args.get('name')
        division = request.args.get('division')
        skilKind = request.args.get('skilKind')
        skil = request.args.get('skil')

        logging.debug('---------------SEARCH---------------')
        logging.debug('dept : ' + dept)
        logging.debug('name : ' + name)
        logging.debug('division : ' + division)
        logging.debug('skilKind : ' + skilKind)
        logging.debug('skil : ' + skil)
        logging.debug('------------------------------------')

        mysql_con = pymysql.connect(host='218.151.225.142', port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT A.EMP_NO AS EMP_NO," \
                             "A.EMP_NAME," \
                             "CASE WHEN A.DEPT ='01' THEN 'FIC'" \
                                   "WHEN A.DEPT ='02' THEN '전자/제조' " \
                                   "WHEN A.DEPT ='03' THEN '통신'" \
                                   "WHEN A.DEPT ='04' THEN '화학'WHEN A.DEPT ='05' THEN '전략' " \
                                   "WHEN A.DEPT ='06' THEN  'DX'ELSE '미정' END AS EMP_DEPT, CASE " \
                                   "WHEN A.DIVS ='1' THEN '정규직' " \
                                   "WHEN A.DIVS ='2' THEN '프리랜서' ELSE '미정' END AS EMP_GRD, " \
                             "A.DIVS," \
                             "A.DEVP_TEL_NO AS EMP_PHONE, " \
                             "A.DEVP_BDAY AS EMP_BIRTH," \
                             "A.SKIL_DB,A.SKIL_LANG, " \
                             "A.SKIL_WEB,A.SKIL_FRAME, " \
                             "A.SKIL_MID " \
                      "FROM (SELECT FRLC.EMP_NO AS EMP_NO," \
                                   "FRLC.EMP_NAME AS EMP_NAME," \
                                   " '' AS DEPT, '2' AS DIVS," \
                                   "FRLC.DEVP_TEL_NO AS DEVP_TEL_NO," \
                                   "FRLC.DEVP_BDAY AS DEVP_BDAY," \
                                   "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '01' THEN SKIL.SKIL_NM_CD ELSE NULL END  SEPARATOR  ',' ) AS SKIL_DB, " \
                                   "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '02' THEN SKIL.SKIL_NM_CD ELSE NULL END  SEPARATOR  ',' ) AS SKIL_LANG, " \
                                   "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '03' THEN SKIL.SKIL_NM_CD ELSE NULL END  SEPARATOR  ',' ) AS SKIL_WEB," \
                                   "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '04' THEN SKIL.SKIL_NM_CD ELSE NULL END  SEPARATOR  ',' ) AS SKIL_FRAME," \
                                   "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '05' THEN SKIL.SKIL_NM_CD ELSE NULL END  SEPARATOR  ',' ) AS SKIL_MID " \
                            "FROM TB_FRLC_DEVP_INFO  FRLC LEFT OUTER JOIN TB_SKIL_MGNT_M SKIL ON FRLC.EMP_NO = SKIL.EMP_NO " \
                            "WHERE 1=1 AND FRLC.DEVP_USE_YN ='Y' " \
                            "GROUP BY FRLC.EMP_NO " \
                            "UNION " \
                            "SELECT EMP.EMP_NO AS EMP_NO, " \
                                  "EMP.EMP_NAME AS EMP_NAME," \
                                  "EMP.DEPT AS DEPT,'1' AS DIVS, " \
                                  "EMP.DEVP_TEL_NO AS DEVP_TEL_NO, " \
                                  "EMP.DEVP_BDAY AS DEVP_BDAY, " \
                                  "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '01' THEN SKIL.SKIL_NM_CD ELSE NULL END  SEPARATOR  ',' ) AS SKIL_DB," \
                                  "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '02' THEN SKIL.SKIL_NM_CD ELSE NULL END  SEPARATOR  ',' ) AS SKIL_LANG, " \
                                  "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '03' THEN SKIL.SKIL_NM_CD ELSE NULL END  SEPARATOR  ',' ) AS SKIL_WEB, " \
                                  "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '04' THEN SKIL.SKIL_NM_CD ELSE NULL END  SEPARATOR  ',' ) AS SKIL_FRAME," \
                                  "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '05' THEN SKIL.SKIL_NM_CD ELSE NULL END  SEPARATOR  ',' ) AS SKIL_MID " \
                            "FROM TB_EMP_TEST EMP LEFT OUTER JOIN TB_SKIL_MGNT_M SKIL ON EMP.EMP_NO = SKIL.EMP_NO " \
                            "GROUP BY EMP.EMP_NO )A " \
                      "WHERE 1=1 "
                if dept != "":
                    sql += "AND DEPT = '" + dept + "' "
                if name != "":
                    sql += "AND EMP_NAME LIKE '%" + name + "%' "
                if division != "":
                    sql += "AND DIVS = '" + division + "' "
                if skilKind == "1":
                    sql += "AND SKIL_DB LIKE '%" + skil + "%'"
                if skilKind == "2":
                    sql += "AND SKIL_LANG LIKE '%" + skil + "%'"
                if skilKind == "3":
                    sql += "AND SKIL_WEB LIKE '%" + skil + "%'"
                if skilKind == "4":
                    sql += "AND SKIL_FRAME LIKE '%" + skil + "%'"
                if skilKind == "5":
                    sql += "AND SKIL_MID LIKE '%" + skil + "%'"
                logging.debug(sql)

                cursor.execute(sql)
        finally:
            mysql_con.close()

        result2 = cursor.fetchall()

        return result2

class skilMgmtDetl(Resource):
    def get(self):
        return "This is SkilDetail Management API! hohoho"

class prjInpuSave(Resource):
    def post(self):
        params = request.get_json()

        logging.debug("save start")
        empNo = request.form['empNo']
        prjCd = request.form['prjCd']
        slinGrd = request.form['slinGrd']
        divs = request.form['divs']

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
                    sql = "INSERT INTO TB_PRJ_INPU_STAT_MGMT(EMP_NO, PRJ_CD, DIVS, SLIN_GRD, INPU_STRT_DAY, INPU_END_DAY, CNTC_STRT_DAY, CNTC_END_DAY, CRGE_JOB, RMKS, REG_EMP_NO, REG_DATE) " \
                          "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,NOW())"
                    cursor.execute(sql, (empNo, prjCd, divs, slinGrd, inpuStrtDay, inpuEndDay, cntcStrtDay, cntcEndDay, crgeJob, rmks,'admin'))
                    mysql_con.commit()
                else:
                    logging.debug('[skil_app] app.py : modified')
                    sql = "UPDATE TB_PRJ_INPU_STAT_MGMT " \
                          "SET DIVS=%s, SLIN_GRD=%s, INPU_STRT_DAY=%s, INPU_END_DAY=%s,  CNTC_STRT_DAY=%s, CNTC_END_DAY=%s, CRGE_JOB=%s, RMKS=%s, CHG_EMP_NO=%s, CHG_DATE= NOW()" \
                          "WHERE EMP_NO = %s AND PRJ_CD = %s "
                    cursor.execute(sql, (divs, slinGrd, inpuStrtDay, inpuEndDay, cntcStrtDay, cntcEndDay, crgeJob, rmks,'admin', empNo, prjCd))
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
api.add_resource(mariaClass,'/mariaClass')

# 개발자 등록
api.add_resource(devSave, '/devSave')
api.add_resource(devDelete, '/devDelete')

# 프로젝트 등록
api.add_resource(prjSave, '/prjSave')
api.add_resource(prjDelete, '/prjDelete')

# 프로젝트 투입 관리
api.add_resource(prjInpuSearch, '/prjInpuSearch')
api.add_resource(prjInpuDelete, '/prjInpuDelete')
api.add_resource(prjInpuSave, '/prjInpuSave')


# 스킬관리
api.add_resource(skilMgmtDetl, '/skilMgmtDetl')
api.add_resource(skilMgmtSearch, '/skilMgmtSearch')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=True)