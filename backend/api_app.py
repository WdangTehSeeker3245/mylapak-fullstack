from datetime import timedelta
from flask import Flask,request,make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import os
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity,get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)
CORS(app)

ACCESS_EXPIRES = timedelta(hours=1)
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "dummytestapp74" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

# basedir = os.path.dirname(os.path.abspath(__file__))
# database = "sqlite:///" + os.path.join(basedir,"db.sqlite")
# app.config["SQLALCHEMY_DATABASE_URI"] = database

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://admin:adminizaus@localhost/mylapak_db"
# app.config["SECRET_KEY"] = "dummytestapp74"

db.init_app(app)

##### Model Class #####

class MyLapakModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_lapak = db.Column(db.String(255))
    title_lapak =  db.Column(db.String(255))
    price = db.Column(db.Integer)
    short_description = db.Column(db.String(255))
    description_lapak = db.Column(db.Text)
   

    # method for save data
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

class AuthModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(225))

    # method untuk menyimpan data
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

# Create Database
with app.app_context():
    db.create_all()

##### Api Class #####

# Administration
class Login(Resource):
    def post(self):
            dataUsername = request.json["username"]
            dataPassword = request.json["password"]
            data = db.session.execute(db.select(AuthModel).filter_by(username=dataUsername)).scalar_one()
            user = data.username
            hashPassword = data.password
            if user:
                authenticated_user = bcrypt.check_password_hash(hashPassword, dataPassword)
                if authenticated_user :
                    access_token = create_access_token(identity=user,expires_delta=ACCESS_EXPIRES)
                    response = {
                        "msg" :"anda berhasil login",
                        "code" : 200,
                        "username" : user,
                        "token" : access_token
                    }
                    return make_response(jsonify(response))

class Register(Resource):
    def post(self):
        dataUsername = request.json["username"]
        dataEmail  = request.json["email"]
        dataPassword = request.json["password"]
        hashPasswd = bcrypt.generate_password_hash(dataPassword)
        model = AuthModel(username=dataUsername,email=dataEmail,password=hashPasswd)
        model.save()

        response = {
            "msg":"data berhasil dimasukan",
            "code": 200
        }
        return make_response(jsonify(response))  

class Admin(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        response = {
            "msg" :"Selamat datang Admin "+current_user,
            "code" : 200 ,
        }
        return make_response(jsonify(response), 200)

class AdminPage(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        response = {
            "msg" :"Authorized Access Admin "+current_user,
            "code" : 200 ,
        }
        return make_response(jsonify(response), 200)

class MyLapakInsert(Resource):
    @jwt_required()
    def post(self):
        # dataImageLapak = request.json["image_lapak"]
        # dataTitleLapak = request.json["html_note"]

        mylapak = MyLapakModel(
            img_lapak=request.json["image_lapak"],
            title_lapak=request.json["title_lapak"],
            price=request.json["price"],
            short_description=request.json["short_description"],
            description_lapak=request.json["description_lapak"]
        )
        mylapak.save()

        response = {
            "msg":"data berhasil dimasukan",
            "code": 200
        }

        return make_response(jsonify(response), 200)

class MyLapakUpdate(Resource):
    @jwt_required()
    def put(self,id):
        query = MyLapakModel.query.get(id)
        editImg = request.json["image_lapak"]
        editTitle = request.json["title_lapak"]
        editPrice = request.json["price"]
        editShdesc = request.json["short_description"]
        editDesc = request.json["description_lapak"]

        query.img_lapak = editImg
        query.title_lapak = editTitle
        query.price = editPrice
        query.short_description = editShdesc
        query.description_lapak = editDesc

        db.session.commit()

        response = {
            "msg":"data berhasil diedit",
            "code": 200
        }
        return make_response(jsonify(response), 200)

class MyLapakAdminView(Resource):
    def get(self,id):
        query = MyLapakModel.query.filter_by(id=id).first()

        output = {
                "id"   : query.id,
                "img_lapak" : query.img_lapak,
                "title_lapak" : query.title_lapak,
                "price" : query.price,
                "short_description" : query.short_description,
                "description_lapak" : query.description_lapak
        }

        response = {
            "code" : 200,
            "msg"  : "Query Data Success",
            "data" : output
        }

        return make_response(jsonify(response), 200)

class MyLapakDelete(Resource):
    @jwt_required()
    def delete(self,id):
        queryData = MyLapakModel.query.get(id)
        
        db.session.delete(queryData)
        db.session.commit()

        response = {
            "msg":"data berhasil dihapus",
            "code": 200
        }
        return make_response(jsonify(response), 200)

# My Lapak Frontend 
class MyLapakList(Resource):
    def get(self):
        query = MyLapakModel.query.all()

        output = [
            {
                "id"   : data.id,
                "img_lapak" : data.img_lapak,
                "title_lapak" : data.title_lapak,
                "price" : data.price,
                "short_description" : data.short_description
            } 
            for data in query
        ]

        response = {
            "code" : 200,
            "msg"  : "Query Data Success",
            "data" : output
        }

        return make_response(jsonify(response), 200)

class MyLapakView(Resource):
    def get(self,id):
        query = MyLapakModel.query.filter_by(id=id).first()

        output = {
                "id"   : query.id,
                "img_lapak" : query.img_lapak,
                "title_lapak" : query.title_lapak,
                "price" : query.price,
                "description_lapak" : query.description_lapak
        }

        response = {
            "code" : 200,
            "msg"  : "Query Data Success",
            "data" : output
        }

        return make_response(jsonify(response), 200)





# Auth
api.add_resource(Login,'/api/login', methods=["POST"])
api.add_resource(Register,'/api/register', methods=["POST"])
api.add_resource(Admin,'/api/admin', methods=["POST"])
api.add_resource(AdminPage,'/api/adminpage', methods=["POST"])

# CRUD
api.add_resource(MyLapakInsert,'/api/insertlapak', methods=["POST"])
api.add_resource(MyLapakUpdate,'/api/updatelapak/<id>', methods=["PUT"])
api.add_resource(MyLapakList,'/api/listlapak', methods=["GET"])
api.add_resource(MyLapakView,'/api/viewlapak/<id>', methods=["GET"])
api.add_resource(MyLapakAdminView,'/api/viewlapakadmin/<id>', methods=["GET"])
api.add_resource(MyLapakDelete,'/api/deletelapak/<id>', methods=["DELETE"])

if __name__ == '__main__':
    app.run(debug=True)