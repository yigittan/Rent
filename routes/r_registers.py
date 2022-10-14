from flask import Blueprint, jsonify, request

r_register = Blueprint('r_register', __name__)


@r_register.route('/register/customers', methods=['POST'])
def customer():
    import app
    body = request.get_json()
    name = body['name']
    surname = body['surname']
    username = body['username']
    email = body['email']
    password = body['password']
    city = body['city']
    wallet = 0
    rented_cars = []
    customer = app.Customer(name, surname, username, email,
                            password, city, wallet, rented_cars)
    res = app.customers_service.create(customer)
    return jsonify(res)


@r_register.route('/register/stores', methods=['POST'])
def stores():
    import app
    body = request.get_json()
    name = body['name']
    city = body['city']
    cars = []
    email = body['email']
    password = body['password']
    store_wallet = 0
    store = app.Store(name, city, cars, email, password, store_wallet)
    res = app.stores_service.create(store)
    return jsonify(res)
