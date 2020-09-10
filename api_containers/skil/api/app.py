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
                    sql = "INSERT INTO TB_FRLC_DEVP_INFO VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (name, rank, grd, tlno, divs, blco, bday, rmks, use_yn))
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
            prgrs_stus = request.form['prgrs_stus']
            # req_skil = request.form['req_skil']
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
                    sql = "INSERT INTO TB_PRJ_INFO VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (prj_nm, cnct_cd, gnr_ctro, ctro, cnct_amt, slin_bzdp, job_divs, prgrs_stus, rmks, '1', use_yn))
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

api.add_resource(Hello, '/hello')
api.add_resource(Register, '/register')
api.add_resource(Retrieve, '/retrieve')
api.add_resource(Save, '/save')
api.add_resource(mariaClass,'/mariaClass')
api.add_resource(devSave, '/devSave')
api.add_resource(prjSave, '/prjSave')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=True)