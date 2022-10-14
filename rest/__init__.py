from flask import request, session, jsonify
from datetime import datetime, timedelta
from customers.customer import Customer
from stores.store import Store

import jwt


from .restcars import register_routes as register_cars_routes
from .restcustomers import register_routes as register_customers_routes
from .reststores import register_routes as register_stores_routes


def register_all_routes(app, cars_service, customers_service, stores_service):
    register_cars_routes(app, cars_service, customers_service, stores_service)
    register_customers_routes(app)
    register_stores_routes(
        app, cars_service, customers_service, stores_service)

    register_routes(app, customers_service, stores_service)


def register_routes(
    app,
    customers_service,
    stores_service,
):
    @app.route('/')
    def home():
        return 'HOme Page'

    @app.route('/logout')
    def logout():
        session.clear()
        return {'message': 'Exit'}

    @app.route('/register/customers', methods=['POST'])
    def customer():
        body = request.get_json()
        name = body['name']
        surname = body['surname']
        username = body['username']
        email = body['email']
        password = body['password']
        city = body['city']
        wallet = 0
        rented_cars = []
        customer = Customer(name, surname, username, email,
                            password, city, wallet, rented_cars)
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
        store_wallet = 0
        store = Store(name, city, cars, email, password, store_wallet)
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

    def login_customer(token, email):
        customer = customers_service.get_customer_by_email(email)
        session['customer'] = True
        session['id'] = customer['id']
        session['email'] = email
        session['token'] = token

    def login_store(token, email):
        store = stores_service.get_store_by_email(email)
        session['store'] = True
        session['id'] = store['id']
        session['token'] = token
