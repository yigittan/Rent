from flask import request
from cars.car import Car


def register_routes(
    app,
    cars_service,
    customers_service,
    stores_service
):
    @app.route('/stores/<string:store_id>', methods=['GET', 'PUT', 'POST', 'DELETE'], endpoint='store/<string:store_id>')
    def store(store_id):
        if request.method == 'POST':
            return create_car(store_id)

        if request.method == 'PUT':
            return update_car(store_id)

        if request.method == 'DELETE':
            return delete_car(store_id)

        if request.method == 'GET':
            return cars_service.get_all_car_by_id(store_id)

    @app.route('/stores/<string:store_id>/<string:car_id>', methods=['POST'], endpoint='stores/<string:store_id>/<string:car_id>')
    def cancel(store_id, car_id):
        car = cars_service.get_car_by_id(car_id)
        res = cars_service.cancel_car(car_id)
        if (res):
            customer = customers_service.get_all_customers(car_id)
            return customers_service.pay_back(customer, car)
        else:
            return 'The car did not rent by someone'

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
