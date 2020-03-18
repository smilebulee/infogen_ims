from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import logging
logging.basicConfig(level=logging.DEBUG)
import bcrypt

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
        logging.debug(request)
        logging.debug(request.get_json())
        logging.debug(request.get_data())
        logging.debug(request.form['email'])

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
            logging.debug("OUT")
            retJson = {
                "status": 301,
                "msg": "Already Exists EMAIL"
            }
            return jsonify(retJson)

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


#
api.add_resource(Hello, '/hello')
api.add_resource(Save, '/save')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)