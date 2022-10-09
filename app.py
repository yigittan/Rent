from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import jwt
from datetime import datetime, timedelta


from users.User import User
from users.users_service import UserService
from users.users_storage import UserMongoStorage
from cars.Car import Car
from cars.cars_service import CarService
from cars.cars_storage import CarMongoStorage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_123'

client = PyMongo(app, uri='mongodb://localhost:27017/Rent')

user_storage = UserMongoStorage(client)
users_service = UserService(user_storage)
car_storage = CarMongoStorage(client)
cars_service = CarService(car_storage)


@app.route('/')
def index():
    return 'INdex Page'


@app.route('/register', methods=['POST'])
def register():
    body = request.get_json()
    name = body['name']
    surname = body['surname']
    username = body['username']
    email = body['email']
    password = body['password']
    city = body['city']
    role = 'customer'

    res = users_service.create(
        User(name, surname, username, email, password, city, role))
    return res


@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    email = body['email']
    c_password = body['password']
    res = users_service.login(email, c_password)
    if res:
        user = users_service.get_user_by_email(email)
        access_token = jwt.encode({
            'name':user['name'],
            'username':user['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=120))
        } , app.config['SECRET_KEY'])
        return access_token
    return {'msg': 'token could not created'}

@app.route('/<string:user_id>/cars' , methods = ['POST'])
def cars(user_id):
    body = request.get_json()
    if request.method == 'POST':
        user = users_service.get_user_by_id(user_id)
        if user['role'] == 'business':
            name = body['name']
            brand = body['brand']
            model_year = body['model_year']
            color = body['color']
            price = body['price']
            status = 'available'
            store_id = user_id
            km = body['km']
            city = body['city']
            car = Car(name,brand,model_year,color,price,status,store_id,km,city)
            res = cars_service.create(car)
            return jsonify(res)
        else:
            return 'Kullanıcı için yetki izni verilmedi'
    return 'Method izni verilmedi'

@app.route('/cars/<string:car_id>', methods = ['GET'])
def car_id(car_id):
    res = cars_service.car_by_id(car_id)
    return jsonify(res)

@app.route('/cars/filter' , methods = ['GET'])
def filter():
    arg = request.args
    store_id = arg.get('store_id')
    name = arg.get('name')
    color = arg.get('color')
    brand = arg.get('brand')
    price = arg.get('price')
    city = arg.get('city')
    model_year = arg.get('model_year')
    filter_query = {}

    if store_id is not None:
        filter_query.update({'store_id':store_id})
    if name is not None:
        filter_query.update({'name':name})
    if color is not None:
        filter_query.update({'color':color})
    if brand is not None:
        filter_query.update({'brand':brand})
    if price is not None:
        filter_query.update({'price':price})
    if city is not None:
        filter_query.update({'city':city})
    if model_year is not None:
        filter_query.update({'model_year':model_year})
    cars_service.filter(filter_query)






if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3000)
