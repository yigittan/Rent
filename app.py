from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import Flask, jsonify, request, session
from flask_pymongo import PyMongo

from cars.cars_service import CarService
from cars.cars_storage import CarMongoStorage
from customers.customers_service import CustomerService
from customers.customers_storage import CustomerMongoStorage
from models.car import Car
from models.customer import Customer
from models.store import Store
from routes.r_cars import r_cars
from routes.r_generals import r_general
from routes.r_registers import r_register
from routes.r_stores import r_store
from stores.stores_service import StoreService
from stores.stores_storage import StoreMongoStorage

app = Flask(__name__)

client = PyMongo(app, uri='mongodb://localhost:27017/Rent')

app.config['SECRET_KEY'] = 'secret_key'
secret_key = app.config['SECRET_KEY']

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
    session['email'] = email
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


def filter():
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


def create_car(store_id):
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


def update_car(store_id):
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


def delete_car(store_id):
    body = request.get_json()
    car_id = body['car_id']
    cars_service.delete_car(car_id)
    stores_service.delete_car(store_id, car_id)
    return car_id


def create_token(store_id, store_name, secret_key):
    token = jwt.encode({
        "id": store_id,
        "name": store_name,
        "exp": (datetime.now() + timedelta(seconds=300)).timestamp()
    }, key=secret_key)
    return token


app.register_blueprint(r_store, url_prefix='/stores')

app.register_blueprint(r_register, url_prefix='/register')

app.register_blueprint(r_cars, url_prefix='/cars')

app.register_blueprint(r_general)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3000)
