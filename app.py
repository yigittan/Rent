from flask import Flask
from flask_pymongo import PyMongo

from customers.customers_service import CustomerService
from customers.customers_storage import CustomerMongoStorage
from stores.stores_service import StoreService
from stores.stores_storage import StoreMongoStorage
from cars.cars_service import CarService
from cars.cars_storage import CarMongoStorage

import rest


app = Flask(__name__)

client = PyMongo(app, uri='mongodb://localhost:27017/Rent')

app.config['SECRET_KEY'] = 'secret_key'

customer_storage = CustomerMongoStorage(client)
customers_service = CustomerService(customer_storage)

store_storage = StoreMongoStorage(client)
stores_service = StoreService(store_storage)

car_storage = CarMongoStorage(client)
cars_service = CarService(car_storage)

rest.register_all_routes(app, cars_service, customers_service, stores_service)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3000)
