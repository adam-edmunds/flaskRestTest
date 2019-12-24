from flask import Flask, render_template, request
from flask_restful import Resource, Api

from string import digits, ascii_letters as letters
from random import choices
import sqlite3 as sql
import datetime

app = Flask(__name__,template_folder="templates")
api = Api(app)

@app.route("/")
def index():
    return render_template("index.html")

class apiEnd(Resource):
    def get(self):
        prefix="AkIDw2P4"
        apiKey = "".join(choices(digits+letters,k=15))
        return {"apiKey":f"{prefix}.{apiKey}","date-created":f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
    def post(self):
        someJSON = request.get_json()
        return {"message":someJSON}, 201

class apiAuth(Resource):
    def get(self):
        apiKey = request.args.get("apikey")
        db = sql.connect("database.db")
        cur = db.cursor()
        try:
            validKey = str(cur.execute(f"SELECT apiKey from apiKeys WHERE apikey = '{apiKey}';").fetchone()[0] is not None)
            return {"validated":validKey}
        except:
            return{"validated":"false"}

class apiAddUser(Resource):
    def post(self):
        db = sql.connect("database.db")
        cur = db.cursor()
        with open("test.txt","w") as file:
            file.write(str(request.headers)+"   "+str(datetime.datetime.now()))
        try:
            cur.execute(f"INSERT INTO users('userName','userPass','dateJoined') VALUES('{request.args.get('username')}','{request.args.get('password')}','{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')")
            db.commit()
            db.close()
            return {"message":"success","object":{"username":request.args.get('username'),"password":request.args.get('password'),"date-joined":f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}},201
        except Exception as e:
            return{"error":str(e)}

class apiGetUser(Resource):
    def get(self):
        db = sql.connect("database.db")
        cur = db.cursor()
        data = cur.execute(f"SELECT * FROM users WHERE userName = '{request.args.get('username')}'").fetchmany()[0]
        return {"data":{"username":data[1],"password":data[2],"date-joined":f'{data[3]}'}}

api.add_resource(apiEnd,"/api/genKey")
api.add_resource(apiAuth,"/api/auth")
api.add_resource(apiAddUser,"/api/addUser")
api.add_resource(apiGetUser,"/api/getUser")

if __name__ == "__main__":
    app.run(debug=True)