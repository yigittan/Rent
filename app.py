from flask import Flask, request, jsonify, session
from flask_pymongo import PyMongo
import jwt
from datetime import datetime, timedelta
from functools import wraps

from customers.Customer import Customer
from customers.customers_service import CustomerService
from customers.customers_storage import CustomerMongoStorage
from stores.Store import Store
from stores.stores_service import StoreService
from stores.stores_storage import StoreMongoStorage
from cars.Car import Car
from cars.cars_service import CarService
from cars.cars_storage import CarMongoStorage


app = Flask(__name__)

client = PyMongo(app, uri='mongodb://localhost:27017/Rent')

app.config['SECRET_KEY'] = 'secret_key'

customer_storage = CustomerMongoStorage(client)
customers_service = CustomerService(customer_storage)

store_storage = StoreMongoStorage(client)
stores_service = StoreService(store_storage)

car_storage = CarMongoStorage(client)
cars_service = CarService(car_storage)


def login_customer(token, email):
    customer = customers_service.get_customer_by_email(email)
    session['customer'] = True
    session['id'] = customer['id']
    session['token'] = token


def auth_customer(func):
    def wrapper(*args, **kwargs):
        if 'customer' in session:
            return func(*args, **kwargs)
        else:
            return {'message': 'Customer not found'}
    return wrapper


def login_store(token, email):
    store = stores_service.get_store_by_email(email)
    session['store'] = True
    session['id'] = store['id']
    session['token'] = token


def auth_store(func):
    def wrapper(*args, **kwargs):
        if 'store' in session:
            return func(*args, **kwargs)
        else:
            return {'message': 'Please Log in'}
    return wrapper


@app.route('/')
def home():
    return 'HOme Page'

@app.route('/logout')
def logout():
    session.clear()
    return {'message':'Exit'}


@app.route('/register/customers', methods=['POST'])
def customer():
    body = request.get_json()
    name = body['name']
    surname = body['surname']
    username = body['username']
    email = body['email']
    password = body['password']
    city = body['city']
    customer = Customer(name, surname, username, email, password, city)
    res = customers_service.create(customer)
    return jsonify(res)


@app.route('/register/stores', methods=['POST'])
def stores():
    body = request.get_json()
    name = body['name']
    city = body['city']
    cars = []
    email = body['email']
    password = body['password']
    store = Store(name, city, cars, email, password)
    res = stores_service.create(store)
    return jsonify(res)


@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    email = body['email']
    c_password = body['password']
    customer = customers_service.login(email, c_password)
    store = stores_service.login(email, c_password)
    if store:
        store = stores_service.get_store_by_email(email)
        token = jwt.encode({
            "id": store['id'],
            "name": store['name'],
            "expiration": str(datetime.utcnow() + timedelta(seconds=120))
        }, key=app.config['SECRET_KEY'])
        login_store(token, email)
        return token
    elif customer:
        customer = customers_service.get_customer_by_email(email)
        token = jwt.encode({
            "id": customer['id'],
            "name": customer['name'],
            "expiration": str(datetime.utcnow() + timedelta(seconds=240))
        }, key=app.config['SECRET_KEY'])
        login_customer(token, email)
        return token
    else:
        return 'Pleasse check your information'


@app.route('/stores/<string:store_id>', methods=['GET', 'PUT', 'POST', 'DELETE'], endpoint='store/<string:store_id>')
@auth_store
def store(store_id):
    if request.method == 'POST':
        store = stores_service.get_store_by_id(store_id)
        body = request.get_json()
        name = body['name']
        brand = body['brand']
        color = body['color']
        model_year = body['model_year']
        price = body['price']
        store_id = store_id
        km = body['km']
        city = store['city']
        rent = "available"
        car = Car(name, brand, color, model_year,
                  price, store_id, km, city, rent)
        car_id = cars_service.create(car)
        stores_service.add_car(car, store_id, car_id)
        return car_id

    if request.method == 'PUT':
        store = stores_service.get_store_by_id(store_id)
        body = request.get_json()
        car_id = body['car_id']
        name = body['name']
        brand = body['brand']
        color = body['color']
        model_year = body['model_year']
        price = body['price']
        store_id = store_id
        km = body['km']
        city = store['city']
        rent = body['rent']
        car = Car(name, brand, color, model_year,
                  price, store_id, km, city, rent)
        cars_service.update_car(car, car_id)
        stores_service.update_car(car, store_id, car_id)
        return car_id

    if request.method == 'DELETE':
        body = request.get_json()
        car_id = body['car_id']
        cars_service.delete_car(car_id)
        stores_service.delete_car(store_id, car_id)
        return car_id

    if request.method == 'GET':
        cars = cars_service.get_all_car_by_id(store_id)
        return cars

@app.route('/cars', methods=['GET'])
def cars():
    arg = request.args
    name = arg.get('name')
    brand = arg.get('brand')
    color = arg.get('color')
    model_year = arg.get('model_year')
    city = arg.get('city')
    price = arg.get('price')
    search_query = {}
    if name is not None:
        search_query.update({'name': name})
    if brand is not None:
        search_query.update({'brand': brand})
    if color is not None:
        search_query.update({'color': color})
    if model_year is not None:
        search_query.update({'model_year': model_year})
    if city is not None:
        search_query.update({'city': city})
    if price is not None:
        search_query.update({'price': price})
    return cars_service.filter(search_query)


@app.route('/cars/<string:car_id>', methods=['POST','GET'], endpoint='cars/<string:car_id>') #wrapper birden çok yerden kullanıldığında nerde kullanıldığını endpoint olarak belirt
@auth_customer
def rent(car_id):
    if request.method == 'POST':
        return cars_service.rent(car_id)
    
    if request.method == 'GET':
        return cars_service.get_car_by_id(car_id)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3000)
