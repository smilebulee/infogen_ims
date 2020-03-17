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
        logging.debug(request.form['email'])

        data = request.get_json()
        logging.debug(data)
        # get data
        email = data["email"]
        password = data["password"]
        addr = data["addr"]
        sex = data["sex"]

        logging.debug(email)
        logging.debug(password)
        logging.debug(addr)
        logging.debug(sex)

        foxTestDb.insert({
            "email": email,
            "password": password,
            "addr": addr,
            "sex": sex
        })

        retJson = {
            "status": 200,
            "msg": "Message has been saved successfully"
        }

        return jsonify(retJson)


#
api.add_resource(Hello, '/hello')
api.add_resource(Save, '/save')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)