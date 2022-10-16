from flask import Blueprint, jsonify, request

r_store = Blueprint('r_store', __name__)


@r_store.route('/<string:store_id>', methods=['GET', 'PUT', 'POST', 'DELETE'], endpoint='store/<string:store_id>')
# @auth_store
def store(store_id):
    import app
    if request.method == 'POST':
        return app.create_car(store_id)

    if request.method == 'PUT':
        return app.update_car(store_id)

    if request.method == 'DELETE':
        return app.delete_car(store_id)

    if request.method == 'GET':
        cars = app.cars_service.get_all_car_by_id(store_id)
        return cars


@r_store.route('/<string:store_id>/<string:car_id>', methods=['POST'], endpoint='stores/<string:store_id>/<string:car_id>')
# @auth_store
def cancel(store_id, car_id):
    import app
    car = app.cars_service.get_car_by_id(car_id)
    res = app.cars_service.cancel_car(car_id)
    if (res):
        customer = app.customers_service.get_all_customers(car_id)
        if customer is None:
            return 'Customer did not rent this car motherfucker'
        app.stores_service.update_store_wallet(store_id,car)
        res = app.customers_service.pay_back(customer, car)
        app.cars_service.update_car_rent(car_id)
        return car_id
    else:
        return 'The car did not rent by someone'
