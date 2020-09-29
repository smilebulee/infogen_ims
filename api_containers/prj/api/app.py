from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://prj_db:27017")
db = client.projectDB
users = db["Users"]

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

        mysql_con = pymysql.connect(host='218.151.225.142', port=3306, db='IFG_IMS', user='ims2', password='1234',
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

        mysql_con = pymysql.connect(host='218.151.225.142', port=3306, db='IFG_IMS', user='ims2', password='1234',
                                    charset='utf8')

        try:
            with mysql_con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT " \
                      "PRJ_CD, SKIL_DIVS, SKIL_NAME " \
                      "FROM TB_PRJ_REQ_SKIL A " \
                      "WHERE PRJ_CD = %s;"
                cursor.execute(sql, prj_cd)
                logging.debug('retrieveReqSkil SUCCESS')
        finally:
            mysql_con.close()

        result = cursor.fetchall()
        logging.debug(result)

        return result



api.add_resource(Hello, '/hello')
api.add_resource(Register, '/register')
api.add_resource(Retrieve, '/retrieve')
api.add_resource(Save, '/save')
api.add_resource(Health, '/health')

# 프로젝트 등록
api.add_resource(retrievePrjInfo, '/retrievePrjInfo')
api.add_resource(retrieveReqSkil, '/retrieveReqSkil')
# api.add_resource(prjSave, '/prjSave')
# api.add_resource(prjDelete, '/prjDelete')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)