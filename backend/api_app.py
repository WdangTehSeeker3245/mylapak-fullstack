from flask import Flask,request,make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from flask_cors import CORS
import os


db = SQLAlchemy()
app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# basedir = os.path.dirname(os.path.abspath(__file__))
# database = "sqlite:///" + os.path.join(basedir,"db.sqlite")
# app.config["SQLALCHEMY_DATABASE_URI"] = database

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root@localhost/mylapak_db"
# app.config["SECRET_KEY"] = "dummytestapp74"

db.init_app(app)

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

# Create Database
with app.app_context():
    db.create_all()

class MyLapakInsert(Resource):
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

class Mencoba(Resource):
    def post(self):
        data = request.get_json()

        return make_response(jsonify(data), 200)

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
    def delete(self,id):
        queryData = MyLapakModel.query.get(id)
        
        db.session.delete(queryData)
        db.session.commit()

        response = {
            "msg":"data berhasil dihapus",
            "code": 200
        }
        return make_response(jsonify(response), 200)

api.add_resource(Mencoba,'/api/mencoba', methods=["POST"])
api.add_resource(MyLapakInsert,'/api/insertlapak', methods=["POST"])
api.add_resource(MyLapakUpdate,'/api/updatelapak/<id>', methods=["PUT"])
api.add_resource(MyLapakList,'/api/listlapak', methods=["GET"])
api.add_resource(MyLapakView,'/api/viewlapak/<id>', methods=["GET"])
api.add_resource(MyLapakAdminView,'/api/viewlapakadmin/<id>', methods=["GET"])
api.add_resource(MyLapakDelete,'/api/deletelapak/<id>', methods=["DELETE"])

if __name__ == '__main__':
    app.run(debug=True)