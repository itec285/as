#!rest-api/bin/python


from flask import Flask, request, jsonify#, HTTPBasicAuth
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import datetime

#Create a engine for connecting to SQLite3
#Assuming starplus.db is in your app root folder

e = create_engine('sqlite:///starplus.db')
#auth = HTTPBasicAuth()

app = Flask(__name__)
api = Api(app)

class StoreCodes_Meta(Resource):
        def get(self):
                #Connect to database
                conn = e.connect()
                #perform query and return JSON data
                query =  conn.execute("Select distinct STORECODE from RDPLogins")
                return {'StoreCodes': [i[0] for i in query.cursor.fetchall()]}

class RDP_Login(Resource):
        def get(self, store_code, auth_code, till_number):
                conn = e.connect()
                query = conn.execute("SELECT * FROM RDPLogins WHERE STORECODE=? AND AUTHCODE = ? and TILLNUMBER = ?",(store_code.upper(), auth_code, till_number))
                #Query the result and get cursor.
                result = {'data': [dict(zip(tuple (query.keys()) ,auth_code)) for auth_code in query.cursor]}
                #To debug result try  >return len(str(result)) or just >return str(result)
                #return jsonify(result)
                return result

class Register(Resource):
        def get(self, store_code, till_number, external_IPAddress, internal_IPAddress):
                now = datetime.datetime.now()
                conn = e.connect()
                query = conn.execute("INSERT INTO Registration(DATE, STORECODE, TILLNUMBER, EXTERNALIPADDRESS, INTERNALIPADDRESS ) VALUES(?,?,?,?,?)", (now, store_code.upper(), till_number, external_IPAddress, internal_IPAddress))

                #Old way
                #return query.lastrowid

                result = {'data':query.lastrowid}
                return jsonify(result)

api.add_resource(StoreCodes_Meta, '/starplus/api/v1.0/storecodes')
api.add_resource(RDP_Login, '/starplus/api/v1.0/rdplogin/<string:store_code>/<string:auth_code>/<string:till_number>')
api.add_resource(Register, '/starplus/api/v1.0/register/<string:store_code>/<int:till_number>/<string:external_IPAddress>/<string:internal_IPAddress>')

if __name__ == '__main__':
#       app.run()
# Do the below to allow from external hosts (dangerous)
        app.run(host='0.0.0.0')
