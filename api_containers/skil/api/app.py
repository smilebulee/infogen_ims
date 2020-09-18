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

            name = request.form['name']
            rank = request.form['rank']
            grd  = request.form['grd']
            tlno = request.form['tlno1'] + request.form['tlno2'] + request.form['tlno3']
            divs = request.form['divs']
            blco = request.form['blco']
            bday = request.form['bday']
            rmks = request.form['rmks']
            use_yn= 'T'

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
                    sql = "INSERT INTO TB_FRLC_DEVP_INFO (`EMP_NO`, " \
                          "`EMP_NAME`, `DEVP_RANK_CD`, `DEVP_GRD_CD`, `DEVP_TLNO`, `DEVP_DIVS_CD`, " \
                          "`DEVP_BLCO`, `DEVP_BDAY`, `REG_EMP_NO`, `REG_DATE`, `CHG_EMP_NO`, `CHG_DATE`, `RMKS`, `DEVP_USE_YN`)  " \
                          "VALUES((SELECT CONCAT('F','_',(SELECT LPAD(COUNT(*)+1,6,'0') FROM TB_FRLC_DEVP_INFO A)))," \
                          "%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, NOW(), %s, %s)"
                    cursor.execute(sql, (name, rank, grd, tlno, divs, blco, bday, 'admin', 'admin', rmks, use_yn))
                    mysql_con.commit()

            finally:
                mysql_con.close()

            result2 = cursor.fetchall()
            for row in result2:
                logging.debug('====== row====')
                logging.debug(row)
                logging.debug('===============')
            # array = list(result2)  # 결과를 리스트로
            #
            # return json.dumps(result2)

            retJson = {
                "status": 200,
                "msg": "Data has been saved successfully"
            }

            return jsonify(retJson)

class prjSave(Resource):
        def post(self):

            params = request.get_json()

            logging.debug("save start")

            prj_nm = request.form['prj_nm']
            cnct_cd = request.form['cnct_cd']
            gnr_ctro = request.form['gnr_ctro']
            ctro = request.form['ctro']
            cnct_amt = request.form['cnct_amt']
            slin_bzdp = request.form['slin_bzdp']
            job_divs = request.form['job_divs']
            pgrs_stus = request.form['pgrs_stus']
            req_skil_divs = request.form['req_skil_divs']
            req_skil_name = request.form['req_skil_name']
            rmks = request.form['rmks']
            use_yn = 'T'

            logging.debug('--------------------------------------')
            logging.debug(prj_nm)
            logging.debug('--------------------------------------')

            logging.debug('================== App Start ==================')
            logging.debug(params)
            logging.debug('================== App End ==================')

            mysql_con = pymysql.connect(host='218.151.225.142', port=3306, db='IFG_IMS', user='ims2', password='1234',
                                        charset='utf8')

            try:
                with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                    sql = "INSERT INTO TB_PRJ_INFO(`PRJ_CD`, `PRJ_NM`, `PRJ_CNCT_CD`, `GNR_CTRO`, `CTRO`, `CNCT_AMT`," \
                          " `SLIN_BZDP`, `JOB_DIVS_CD`, `PRGRS_STUS_CD`, `REG_EMP_NO`, `REG_DATE`, `CHG_EMP_NO`," \
                          " `CHG_DATE`, `RMKS`, `USE_YN`) " \
                          "VALUES((SELECT CONCAT('PRJ','_',(SELECT LPAD(COUNT(*)+1,6,'0') FROM TB_PRJ_INFO A))), " \
                          "%s, %s, %s, %s, %s, %s, %s, %s, 'admin', NOW(), 'admin', NOW(), %s, %s)"
                    cursor.execute(sql, (prj_nm, cnct_cd, gnr_ctro, ctro, cnct_amt, slin_bzdp, job_divs, pgrs_stus, rmks, use_yn))
                    mysql_con.commit()

                    logging.debug('PRJ_INFO SUCCESS')
                    logging.debug(prj_nm + req_skil_divs + req_skil_name)

                    sql = "INSERT INTO TB_PRJ_REQ_SKIL(`PRJ_CD`, `SKIL_DIVS`, `SKIL_NAME`, `REG_EMP_NO`, `REG_DATE`," \
                          " `CHG_EMP_NO`, `CHG_DATE`) " \
                          "VALUES ((SELECT PRJ_CD FROM TB_PRJ_INFO A WHERE PRJ_NM = %s)," \
                          " %s, %s, 'admin', NOW(), 'admin', NOW())"
                    cursor.execute(sql, (prj_nm, req_skil_divs, req_skil_name))
                    mysql_con.commit()

                    logging.debug('REQ_SKIL SUCCESS')

            finally:
                mysql_con.close()

            result2 = cursor.fetchall()
            for row in result2:
                logging.debug('====== row====')
                logging.debug(row)
                logging.debug('===============')
            # array = list(result2)  # 결과를 리스트로
            #
            # return json.dumps(result2)

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
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

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
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

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
                if dept =="" and name == "" and  division =="" and skilKind == "" and skil == "":
                    sql = "SELECT * FROM TB_SKIL_MGNT_TEST"
                    cursor.execute(sql)
                else:
                    sql = "SELECT * FROM TB_SKIL_MGNT_TEST WHERE 1=1 "
                    if dept != "":
                        sql = sql + "AND EMP_DEPT = %s "
                    if name != "":
                        sql = sql + """AND EMP_NAME LIKE %s """
                    if division != "":
                        sql = sql + "AND DIVISION = %s "
                    if skilKind == "1":
                        sql += """AND SKIL_DB LIKE %s"""
                    if skilKind == "2":
                        sql += """AND SKIL_LANG LIKE %s"""
                    if skilKind == "3":
                        sql += """AND SKIL_WEB LIKE %s"""
                    if skilKind == "4":
                        sql += """AND SKIL_FRAME LIKE %s"""
                    if skilKind == "5":
                        sql += """AND SKIL_MID LIKE %s"""
                    logging.debug(sql)

                    cursor.execute(sql, (dept,'%'+name+'%',division,'%'+skil+'%'))
        finally:
            mysql_con.close()

        result2 = cursor.fetchall()
        for row in result2:
            logging.debug('====== row====')
            logging.debug(row)
            logging.debug('===============')
        array = list(result2)  # 결과를 리스트로

        return result2

class skilMgmtDetl(Resource):
    def get(self):
        return "This is SkilDetail Management API! hohoho"

api.add_resource(Hello, '/hello')
api.add_resource(Register, '/register')
api.add_resource(Retrieve, '/retrieve')
api.add_resource(Save, '/save')
api.add_resource(mariaClass,'/mariaClass')
api.add_resource(devSave, '/devSave')
api.add_resource(prjSave, '/prjSave')

# 프로젝트 투입 관리
api.add_resource(prjInpuSearch, '/prjInpuSearch')
api.add_resource(prjInpuDelete, '/prjInpuDelete')

# 스킬관리
api.add_resource(skilMgmtDetl, '/skilMgmtDetl')
api.add_resource(skilMgmtSearch, '/skilMgmtSearch')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=True)