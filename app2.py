from flask import Flask, Response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os 
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()
conn_Str = os.getenv("conn_Str")

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = conn_Str

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, auto_increment = True, primary_key = True)
    name = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(), nullable = False, unique=True)
    password = db.Column(db.String(), nullable = False)

    def to_json(self):
        return {"id": self.id, "name": self.name, "email": self.email}
        
    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

@app.route("/usuarios")
def usuariosget():
    usersob = Users.query.all()
    usersjs = [usuarios.to_json() for usuarios in usersob]

    return usersjs

@app.route("/usuarios/<email>")
def usuarioget(email):
    userob = Users.query.filter_by(email=email).first()
    userjsn = userob.to_json()
    print(userjsn)
    return userjsn

@app.route("/usuarios", methods=["POST"])
def usuariocadastro():
    userdata = request.get_json()
    pwd = generate_password_hash(userdata["password"])
    print(userdata)
    try:
        usr = Users.query.filter_by(email=userdata["email"]).first()
        if usr:
            return jsonify({"ERRO": "JÁ EXISTE UM USUARIO CADASTRADO COM ESTE EMAIL!"}), 409
        
        user = Users(name = userdata["name"], email=userdata["email"], password=pwd)
        db.session.add(user)
        db.session.commit()
        usr = {"id": user.id, "name": user.name, "email": user.email}
        return jsonify({"message": "Usuário cadastrado com sucesso", "user": usr}), 201
    except Exception as e:
        return f"OCORREU UM ERRO {e}"
    
@app.route("/usuarios/<id>", methods=["PUT"])
def usuarioupdt(id):
    userob = Users.query.filter_by(id=id).first()
    userdt = request.get_json()

    try:
        if "name" in userdt:
            userob.name = userdt["name"]
        if "email" in userdt:
            userob.email = userdt["email"]
        if "password" in userdt:
            pwd = generate_password_hash(userdt["password"])
            userob.password = pwd
        db.session.add(userob)
        db.session.commit()
        #return f"{200}, {userdt}, Usuario ATUALIZADO:"
        return jsonify({"message": "Usuário ATUALIZADO com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": "OCORREU UM ERRO", "user": e}), 400
        #return f"ERRO 400 {e}"

@app.route("/usuarios/<id>", methods=["DELETE"])
def userdelet(id):
    try:
        userob = Users.query.filter_by(id=id).first()
        if userob:
            db.session.delete(userob)
            db.session.commit()
            return jsonify({"message": "Usuário DELETADO com sucesso", "user": id}), 200
            #return f"{200}, {userob}, Usuario DELETADO:"
    except Exception as e:
        print(e)
        return jsonify({"message": "ERRO"}), 400
        #return f"ERRO 400: {e}"


@app.route("/login", methods=["POST"])
def loginuser():
    userdt = request.get_json()
    email = userdt["email"]
    senha = userdt["password"]
    print(userdt)
    print("--------------------------------")
    user = Users.query.filter_by(email=email).first()
    print(user)
    if not user or not user.verify_password(senha):
        return jsonify({"error": "Usuário ou senha inválidos"}), 401
    
    #return jsonify({"cod": 200})

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email
    }), 200


app.run()