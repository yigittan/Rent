from flask import Blueprint, jsonify, request

from app import auth_customer

r_cars = Blueprint('r_cars', __name__)


@r_cars.route('/', methods=['GET'])
def cars():
    import app
    return app.filter()


@r_cars.route('/<string:car_id>', methods=['POST', 'GET'], endpoint='/cars/string:car_id')
@auth_customer
def rent(car_id):
    import app
    if request.method == 'POST':
        email = app.session.get('email')
        customer = app.customers_service.get_customer_by_email(email)
        car = app.cars_service.get_car_by_id(car_id)
        store_id = car['store_id']
        print(store_id)
        store = app.stores_service.get_store_by_id(store_id)
        if(app.customers_service.is_available(car, customer)):
            app.stores_service.payment_for_rent(car, store)
            app.cars_service.rent(car_id)
            return "success rented"
        else:
            return 'Money is not enough to rent a car'

    if request.method == 'GET':
        return app.cars_service.get_car_by_id(car_id)
