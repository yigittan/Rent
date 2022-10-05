from flask import Flask , request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager


from users.User import User
from users.users_service import UserService
from users.users_storage import UserMongoStorage

app = Flask(__name__)
jwt =JWTManager(app)

client = PyMongo(app,uri='mongodb://localhost:27017/Rent')

user_storage = UserMongoStorage(client)
users_service = UserService(user_storage)

@app.route('/')
def index():
    return 'INdex Page'

@app.route('/register',methods = ['POST'])
def register():
    body = request.get_json()
    name = body['name']
    surname = body['surname']
    username = body['username']
    email = body['email']
    password = body['password']
    city = body['city']
    role = 'customer'

    res = users_service.create(User(name,surname,username,email,password,city,role))
    return res

@app.route('/login',methods=['POST'])
def login():
    body = request.get_json()
    email = body['email']
    c_password = body['password']
    res = users_service.login(email,c_password)
    if res:
        access_token = create_access_token(identity=res['username'])
        return jsonify(access_token)
    return {'msg':'token could not created'}




    


if __name__ == '__main__':
    app.secret_key = 'ssk_123'
    app.run(debug=True,host='127.0.0.1',port=3000)

