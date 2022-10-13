from crypt import methods
from flask import Blueprint, request
import jwt
from app import store_methods, cars_service


r_stores = Blueprint('r_stores',__name__)

@r_stores.route('/<string:store_id>', methods=['GET','PUT','POST','DELETE']):
def store(store_id):
    bearer_token = request.headers.get('Authorization')
    token = bearer_token.removeprefix('Bearer ')
    payload = jwt.decode(token,key=app.config['SECRET_KEY'])

    if request.method == 'POST':
        return store_methods.create_car(store_id)

    if request.method == 'PUT':
        return store_methods.update_car(store_id)

    if request.method == 'DELETE':
        return store_methods.delete_car(store_id)

    if request.method == 'GET':
        cars = cars_service.get_all_car_by_id(store_id)
        return cars