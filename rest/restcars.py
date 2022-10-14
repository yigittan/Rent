from flask import request, session


def register_routes(
    app,
    cars_service,
    customers_service,
    stores_service
):
    @app.route('/cars', methods=['GET'])
    def cars():
        return filter()

    # wrapper birden çok yerden kullanıldığında nerde kullanıldığını endpoint olarak belirt
    @app.route('/cars/<string:car_id>', methods=['POST', 'GET'], endpoint='cars/<string:car_id>')
    def rent(car_id):
        if request.method == 'POST':
            email = session.get('email')
            customer = customers_service.get_customer_by_email(email)
            car = cars_service.get_car_by_id(car_id)
            store_id = car['store_id']
            print(store_id)
            store = stores_service.get_store_by_id(store_id)
            if (customers_service.is_available(car, customer)):
                stores_service.payment_for_rent(car, store)
                cars_service.rent(car_id)
                return "success rented"
            else:
                return 'Money is not enough to rent a car'

        if request.method == 'GET':
            return cars_service.get_car_by_id(car_id)
