from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import logging
logging.basicConfig(level=logging.DEBUG)
import bcrypt

from bson.json_util import dumps
import json

app = Flask(__name__)
api = Api(app)
logger = logging.getLogger(__name__)

client = MongoClient("mongodb://emp_db:27017")
db = client.local
foxTestDb = db["foxTest"]


""" 
HELPER FUNCTIONS
"""

def existsEmail(email):
    logging.debug(foxTestDb.find({"email": email}).count())
    if foxTestDb.find({"email": email}).count() == 0:
        return False
    else:
        return True


"""
RESOURCES
"""


class Hello(Resource):
    def get(self):
        logging.debug("test")
        return "This is Employee Management API! hohoho"

class Save(Resource):
    def post(self):
        # Get posted data from request
        logging.debug("save start")
        # logging.debug(request)
        # logging.debug(request.get_json())
        # logging.debug(request.get_data())
        # logging.debug(request.form['email'])

        #data = request.get_json()
        # get data
        email = request.form['email']
        password = request.form['password']
        addr = request.form['addr']
        sex = request.form['sex']

        logging.debug('--------------------------------------')
        logging.debug('email : ' + email)
        logging.debug('password : ' + password)
        logging.debug('addr : ' + addr)
        logging.debug('sex : ' + sex)
        logging.debug('--------------------------------------')

        # logging.debug(existsEmail(email))
        if existsEmail(email):
            logging.debug("!!! WARNING !!! email Exists!!")
            retJson = {
                "status": 301,
                "msg": "Already Exists EMAIL"
            }
        else:
            foxTestDb.insert({
                "email": email,
                "password": password,
                "addr": addr,
                "sex": sex
            })
            retJson = {
                "status": 200,
                "msg": "Data has been saved successfully"
            }

        return jsonify(retJson)

class Search(Resource):
    def get(self):
        # Get posted data from request
        logging.debug("search start")

        # get data
        email = request.args.get('email')

        logging.debug('---------------SEARCH---------------')
        logging.debug('email : ' + email)
        logging.debug('------------------------------------')

        if email is None or email == "":
            logging.debug("is None")
            result = foxTestDb.find()
        else:
            logging.debug("is not null")
            result = foxTestDb.find({
                "email": email
            })

        logging.debug('---------------RESULT---------------')
        logging.debug(result)
        logging.debug('------------------------------------')
        array = list(result) #결과를 리스트로
        logging.debug(array)
        logging.debug(dumps(array)) #리스트파일은 dumps
        logging.debug(jsonify(dumps(array))) #dumps한 파일은 jsonify

        # retJson = {
        #     "status": 200,
        #     "msg": "Data has been saved successfully"
        # }

        return jsonify(dumps(array))

#
api.add_resource(Hello, '/hello')
api.add_resource(Save, '/save')
api.add_resource(Search, '/search')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)