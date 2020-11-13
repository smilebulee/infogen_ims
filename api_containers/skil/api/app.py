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

def getSystemInfo():
    logging.debug('skil Server')
    logging.debug(socket.gethostbyname(socket.gethostname()))
    try:

        logging.debug('Skii IP Address Start')
        logging.debug(socket.gethostbyname(socket.gethostname()))
        logging.debug('Skii IP Address End')

        if (socket.gethostbyname(socket.gethostname()) == "172.20.0.7" ) :
            logging.debug('Prod Server')
            return "mariadb"
        else :
            logging.debug('Local Server')
            return "mariadb"

    except Exception as e:
        logging.exception(e)


"""
RESOURCES
"""


class Hello(Resource):
    def get(self):
        mysql_con = pymysql.connect(host='218.151.225.142', port=9876, db='testdb', user='ims2', password='1234',
                                    charset='utf8')
        mysql_con.cursor(pymysql.cursors.DictCursor)
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

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT A.EMP_NO, " \
                              "A.EMP_NAME, " \
                              "A.DEPT_CD," \
                              "DEPT.CMM_CD_NAME AS DEPT_NM," \
                              "A.CNTC_DIVS_CD, " \
                              "CNTC.CMM_CD_NAME AS CNTC_DIVS_NM, " \
                              "A.SKIL_DB,A.SKIL_LANG,A.SKIL_WEB," \
                              "A.SKIL_FRAME, A.SKIL_MID, " \
                              "A.DEVP_TEL_NO," \
                              "A.DEVP_BDAY " \
                      "FROM (SELECT FRLC.EMP_NO AS EMP_NO, " \
                                  "FRLC.EMP_NAME AS EMP_NAME, " \
                                  "FRLC.EMP_DEPT_CD AS DEPT_CD, " \
                                  "FRLC.CNTC_DIVS_CD AS CNTC_DIVS_CD, " \
                                  "FRLC.DEVP_TEL_NO AS DEVP_TEL_NO, " \
                                  "FRLC.DEVP_BDAY AS DEVP_BDAY, " \
                                  "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '01' THEN CONCAT('(',(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL CMM WHERE 1=1 AND CMM_CD_GRP_ID = 'SKIL_LVL_CD' AND CMM.CMM_CD = SKIL_LVL_CD),')',SKIL.SKIL_NM_CD) ELSE NULL END  SEPARATOR  ', ' ) AS SKIL_DB, " \
                                  "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '02' THEN CONCAT('(',(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL CMM WHERE 1=1 AND CMM_CD_GRP_ID = 'SKIL_LVL_CD' AND CMM.CMM_CD = SKIL_LVL_CD),')',SKIL.SKIL_NM_CD) ELSE NULL END  SEPARATOR  ', ' ) AS SKIL_LANG, " \
                                  "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '03' THEN CONCAT('(',(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL CMM WHERE 1=1 AND CMM_CD_GRP_ID = 'SKIL_LVL_CD' AND CMM.CMM_CD = SKIL_LVL_CD),')',SKIL.SKIL_NM_CD) ELSE NULL END  SEPARATOR  ', ' ) AS SKIL_WEB, " \
                                  "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '04' THEN CONCAT('(',(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL CMM WHERE 1=1 AND CMM_CD_GRP_ID = 'SKIL_LVL_CD' AND CMM.CMM_CD = SKIL_LVL_CD),')',SKIL.SKIL_NM_CD) ELSE NULL END  SEPARATOR  ', ' ) AS SKIL_FRAME, " \
                                  "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '05' THEN CONCAT('(',(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL CMM WHERE 1=1 AND CMM_CD_GRP_ID = 'SKIL_LVL_CD' AND CMM.CMM_CD = SKIL_LVL_CD),')',SKIL.SKIL_NM_CD) ELSE NULL END  SEPARATOR  ', ' ) AS SKIL_MID " \
                              "FROM TB_FRLC_DEVP_INFO  FRLC LEFT OUTER JOIN TB_SKIL_MGNT_M SKIL ON FRLC.EMP_NO = SKIL.EMP_NO " \
                              "WHERE FRLC.DEVP_USE_YN ='Y' " \
                              "GROUP BY FRLC.EMP_NO  " \
                              "UNION " \
                              "SELECT EMP.EMP_ID AS EMP_NO, " \
                                      "EMP.EMP_NAME AS EMP_NAME, " \
                                      "EMP.DEPT_CD AS DEPT_CD, " \
                                      "'01' AS CNTC_DIVS_CD, " \
                                      "EMP.EMP_TEL AS DEVP_TEL_NO, " \
                                      "EMP.EMP_BDAY AS DEVP_BDAY, " \
                                      "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '01' THEN CONCAT('(',(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL CMM WHERE 1=1 AND CMM_CD_GRP_ID = 'SKIL_LVL_CD' AND CMM.CMM_CD = SKIL_LVL_CD),')',SKIL.SKIL_NM_CD) ELSE NULL END  SEPARATOR  ', ' ) AS SKIL_DB, " \
                                      "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '02' THEN CONCAT('(',(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL CMM WHERE 1=1 AND CMM_CD_GRP_ID = 'SKIL_LVL_CD' AND CMM.CMM_CD = SKIL_LVL_CD),')',SKIL.SKIL_NM_CD) ELSE NULL END  SEPARATOR  ', ' ) AS SKIL_LANG, " \
                                      "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '03' THEN CONCAT('(',(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL CMM WHERE 1=1 AND CMM_CD_GRP_ID = 'SKIL_LVL_CD' AND CMM.CMM_CD = SKIL_LVL_CD),')',SKIL.SKIL_NM_CD) ELSE NULL END  SEPARATOR  ', ' ) AS SKIL_WEB, " \
                                      "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '04' THEN CONCAT('(',(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL CMM WHERE 1=1 AND CMM_CD_GRP_ID = 'SKIL_LVL_CD' AND CMM.CMM_CD = SKIL_LVL_CD),')',SKIL.SKIL_NM_CD) ELSE NULL END  SEPARATOR  ', ' ) AS SKIL_FRAME, " \
                                      "GROUP_CONCAT( CASE SKIL.SKIL_DIVS_CD WHEN '05' THEN CONCAT('(',(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL CMM WHERE 1=1 AND CMM_CD_GRP_ID = 'SKIL_LVL_CD' AND CMM.CMM_CD = SKIL_LVL_CD),')',SKIL.SKIL_NM_CD) ELSE NULL END  SEPARATOR  ', ' ) AS SKIL_MID " \
                              "FROM TB_EMP_MGMT EMP LEFT OUTER JOIN TB_SKIL_MGNT_M SKIL ON EMP.EMP_ID = SKIL.EMP_NO GROUP BY EMP.EMP_ID) A, " \
                              "TB_CMM_CD_DETL CNTC, " \
                              "TB_CMM_CD_DETL DEPT " \
                      "WHERE 1=1 " \
                      "AND A.CNTC_DIVS_CD = CNTC.CMM_CD AND A.DEPT_CD = DEPT.CMM_CD " \
                      "AND CNTC.CMM_CD_GRP_ID ='CNTC_DIVS_CD' " \
                      "AND DEPT.CMM_CD_GRP_ID = 'SLIN_BZDP'"
                if dept != "":
                    sql += "AND DEPT_CD = '" + dept + "' "
                if name != "":
                    sql += "AND EMP_NAME LIKE '%" + name + "%' "
                if division != "":
                    sql += "AND CNTC_DIVS_CD = '" + division + "' "
                if skilKind == "01":
                    sql += "AND SKIL_DB LIKE '%" + skil + "%'"
                if skilKind == "02":
                    sql += "AND SKIL_LANG LIKE '%" + skil + "%'"
                if skilKind == "03":
                    sql += "AND SKIL_WEB LIKE '%" + skil + "%'"
                if skilKind == "04":
                    sql += "AND SKIL_FRAME LIKE '%" + skil + "%'"
                if skilKind == "05":
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

class skilRegPopupSearch(Resource):
    def get(self):
        params = request.get_json()

        logging.debug('skilRegPopupSearch Start')
        empNo = request.args.get('empNo')
        cntcDivsCd = request.args.get('cntcDivsCd')

        logging.debug('skilRegPopupSearch empNo' + empNo)
        logging.debug('skilRegPopupSearch cntcDivsCd' + cntcDivsCd)

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')
        if cntcDivsCd == '01' :
            try:
                with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                    sql = "SELECT A.EMP_NAME," \
                            "A.DEPT_CD," \
                            "A.EMP_RANK_CD," \
                            "B.SKIL_DIVS_CD," \
                            "B.SKIL_NM_CD," \
                            "B.SKIL_LVL_CD," \
                            "A.REMARK," \
                            "'01' AS CNTC_DIVS_CD," \
                            "'정규직' AS CNTN_DIVE_NM," \
                            "(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL A1 " \
                            "WHERE A1.CMM_CD_GRP_ID ='EMP_RANK_CD' " \
                            "AND A1.CMM_CD = A.EMP_RANK_CD " \
                            ") AS EMP_RANK_NM, " \
                            "(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL A1 " \
                            "WHERE A1.CMM_CD_GRP_ID ='SLIN_BZDP' "\
                            "AND A1.CMM_CD = A.DEPT_CD "\
                            ") AS SLIN_BZDP " \
                         "FROM TB_EMP_MGMT A LEFT OUTER JOIN TB_SKIL_MGNT_M B ON A.EMP_ID = B.EMP_NO " \
                         "WHERE A.EMP_ID ='" + empNo + "' "


                    cursor.execute(sql)
                    logging.debug('skilRegPopupSearch SUCCESS')
            finally:
                mysql_con.close()
        else :
            try:
                with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                    sql = "SELECT A.EMP_NAME," \
                            "A.EMP_DEPT_CD," \
                            "A.EMP_RANK_CD," \
                            "B.SKIL_DIVS_CD," \
                            "B.SKIL_NM_CD," \
                            "B.SKIL_LVL_CD," \
                            "A.RMKS," \
                            "(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL A1 " \
                            "WHERE A1.CMM_CD_GRP_ID ='EMP_RANK_CD' " \
                            "AND A1.CMM_CD = A.EMP_RANK_CD " \
                            ") AS EMP_RANK_NM, " \
                            "(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL A1 " \
                            "WHERE A1.CMM_CD_GRP_ID ='SLIN_BZDP' "\
                            "AND A1.CMM_CD = A.EMP_DEPT_CD "\
                            ") AS SLIN_BZDP " \
                            "(SELECT CMM_CD_NAME FROM TB_CMM_CD_DETL A1 " \
                            "WHERE A1.CMM_CD_GRP_ID ='CNTC_DIVS_CD' " \
                            "AND A1.CMM_CD = A.CNTC_DIVS_CD " \
                            ") AS CNTC_DIVS_NM " \
                            "FROM TB_FRLC_DEVP_INFO A LEFT OUTER JOIN TB_SKIL_MGNT_M B ON A.EMP_ID = B.EMP_NO " \
                            "WHERE A.EMP_NO ='" + empNo + "' "


                    cursor.execute(sql)
                    logging.debug('skilRegPopupSearch SUCCESS')
            finally:
                mysql_con.close()

        result1 = cursor.fetchall()
        logging.debug(result1)

        return result1

#스킬 코드 조회
class retrieveEmpSkilCd(Resource):
    def get(self):
        params = request.get_json()

        logging.debug('retrieveskilCd Start')

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT " \
                      "SKIL_DIVS_CD, " \
                      "SKIL_NAME " \
                      "FROM TB_SKIL_MGNT_CD "
                cursor.execute(sql)

                logging.debug('retrieveskilCd SUCCESS')
        finally:
            mysql_con.close()

        result = cursor.fetchall()
        logging.debug(result)

        return result

class deleteSkilDetl(Resource):
    def post(self):
        params = request.get_json()

        logging.debug('deleteSkilDetl Start')

        empNo = request.form['emp_no']

        logging.debug(empNo)

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "DELETE FROM TB_SKIL_MGNT_M WHERE EMP_NO = %s " \

                cursor.execute(sql, empNo)
                mysql_con.commit()
                logging.debug('deleteSkilDetl SUCCESS')
        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been delete successfully"
        }

        return jsonify(retJson)

class saveSkilDetl(Resource):
    def post(self):

        params = request.get_json()

        logging.debug("saveSkilDetl start_01")

        logging.debug(params)

        logging.debug("saveSkilDetl start_02")

        for row in request.form:
            logging.debug(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        empNo = request.form['emp_no']

        logging.debug(empNo)

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:

                sql = "DELETE FROM TB_SKIL_MGNT_M WHERE EMP_NO = %s "

                cursor.execute(sql, empNo)
                mysql_con.commit()
                logging.debug('delete SkilDetl SUCCESS')


                logging.debug('save SkilDetl START')

                for i in range(0, int(table_count)):
                    skil_hight = request.form['skil_hight' + str(i)]
                    logging.debug(skil_hight)
                    if skil_hight != '00':
                        logging.debug('CHECK01')
                        skil_middle = request.form['skil_middle' + str(i)]
                        skil_lvl = request.form['skil_lvl' + str(i)]

                        sql1 = "SELECT IFNULL(MAX(SKIL_SNO) + 1, 1) AS SKIL_SNO FROM TB_SKIL_MGNT_M WHERE EMP_NO = %s"
                        cursor.execute(sql1, empNo)
                        snoResult = cursor.fetchone()
                        skil_sno = snoResult['SKIL_SNO']

                        logging.debug('insert start')
                        sql2 = "INSERT INTO TB_SKIL_MGNT_M(`EMP_NO`, " \
                              "`SKIL_SNO`, "    \
                              "`SKIL_DIVS_CD`, " \
                              "`SKIL_NM_CD`, " \
                              "`SKIL_LVL_CD`, " \
                              "`REG_EMP_NO`, " \
                              "`REG_DATE`," \
                              " `CHG_EMP_NO`, " \
                              "`CHG_DATE`) " \
                              "VALUES (%s, " \
                              "%s, %s, %s, %s, %s, NOW(), %s, NOW())"
                        cursor.execute(sql2, (empNo, skil_sno, skil_hight, skil_middle, skil_lvl, userId, userId))
                        mysql_con.commit()
                        logging.debug('REQ_SKIL' + str(i) + ' SUCCESS')

        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "Data has been save successfully"
        }

        return jsonify(retJson)

class retrieveSkilCd(Resource):
    def get(self):
        # Get posted data from request
        logging.debug("search start")

        # get data
        skilDiv = request.args.get('skilDiv')

        logging.debug('---------------SEARCH---------------')
        logging.debug('skilDiv : ' + skilDiv)
        logging.debug('------------------------------------')

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT SKIL_SNO, SKIL_DIVS_CD, SKIL_NAME, REG_EMP_NO, DATE_FORMAT(REG_DATE, '%Y-%m-%d') AS REG_DATE, RMKS FROM TB_SKIL_MGNT_CD WHERE 1=1 "
                if skilDiv == "":
                    cursor.execute(sql)
                else:
                    sql += "AND SKIL_DIVS_CD = " + skilDiv
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

class getskilCdMgmt(Resource):
    def get(self):
        # Get posted data from request
        logging.debug("getskilCdMgmt Start")

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT CMM_CD, CMM_CD_NAME FROM TB_CMM_CD_DETL WHERE CMM_CD_GRP_ID = 'SKIL_DIVS_CD' ORDER BY CMM_CD ASC"

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

#스킬 코드 삭제
class deleteSkilCd(Resource):
    def post(self):
        params = request.get_json()

        logging.debug("deleteSkilCd start")
        skil_sno = request.form['skilSno']

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2',
                                    password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "DELETE FROM TB_SKIL_MGNT_CD " \
                      "WHERE SKIL_SNO = %s"
                cursor.execute(sql, skil_sno)
                mysql_con.commit()
                logging.debug('deleteSkilCd success')
        finally:
            mysql_con.close()

        retJson = {
            "status": 200,
            "msg": "deleteSkilCd success"
        }

        return jsonify(retJson)

#스킬 코드 insert
class insertSkilCd(Resource):
    def post(self):
        params = request.get_json()

        logging.debug("insertSkilCd Start")

        for row in request.form:
            logging.debug(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')
        logging.debug("CONNET Start")
        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                logging.debug("SQL Start")
                sql = "SELECT MAX(SKIL_SNO) + 1 AS SKIL_SNO FROM TB_SKIL_MGNT_CD"
                cursor.execute(sql)
                snoResult = cursor.fetchone()
                skil_sno = snoResult['SKIL_SNO']
                logging.debug(skil_sno)

                sql2 = "INSERT INTO TB_SKIL_MGNT_CD (`SKIL_SNO`, " \
                      "`SKIL_DIVS_CD`, " \
                      "`SKIL_NAME`, " \
                      "`REG_EMP_NO`, " \
                      "`REG_DATE`, " \
                      "`CHG_EMP_NO`, " \
                      "`CHG_DATE`, " \
                      "`RMKS`) " \
                      "VALUES(%s, %s, %s, %s, NOW(), %s, NOW(), %s)"

                cursor.execute(sql2, (skil_sno, SKIL_DIVS_CD, SKIL_NAME, userId, REG_DATE, RMKS))
                mysql_con.commit()

        finally:
            mysql_con.close()

        return skil_sno

#스킬 코드 update
class updateSkilCd(Resource):
    def post(self):
        params = request.get_json()

        logging.debug("updateSkilCd Start")

        for row in request.form:
            logging.debug(row + ':' + request.form[row])
            globals()[row] = request.form[row]

        mysql_con = pymysql.connect(getSystemInfo(), port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "UPDATE TB_SKIL_MGNT_CD " \
                        "SET SKIL_DIVS_CD=%s, SKIL_NAME=%s, REG_EMP_NO=%s, REG_DATE=NOW(), RMKS=%s" \
                        "WHERE SKIL_SNO = %s"

                cursor.execute(sql, (SKIL_DIVS_CD, SKIL_NAME, userId, RMKS, SKIL_SNO))
                mysql_con.commit()

        finally:
            mysql_con.close()

        return skil_sno

api.add_resource(Hello, '/hello')
api.add_resource(Register, '/register')
api.add_resource(Retrieve, '/retrieve')
api.add_resource(Save, '/save')
api.add_resource(mariaClass,'/mariaClass')

# 스킬관리
api.add_resource(skilMgmtDetl, '/skilMgmtDetl')
api.add_resource(skilMgmtSearch, '/skilMgmtSearch')

#공통 코드 조회
api.add_resource(retrieveCmmCd, '/retrieveCmmCd')

# 스킬 상세 관리
api.add_resource(skilRegPopupSearch, '/skilRegPopupSearch')
api.add_resource(retrieveEmpSkilCd, '/retrieveEmpSkilCd')
api.add_resource(deleteSkilDetl, '/deleteSkilDetl')
api.add_resource(saveSkilDetl, '/saveSkilDetl')


# 스킬 코드 관리
api.add_resource(retrieveSkilCd, '/retrieveSkilCd')
api.add_resource(getskilCdMgmt, '/getskilCdMgmt')
api.add_resource(deleteSkilCd, '/deleteSkilCd')
api.add_resource(insertSkilCd, '/insertSkilCd')
api.add_resource(updateSkilCd, '/updateSkilCd')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=True)