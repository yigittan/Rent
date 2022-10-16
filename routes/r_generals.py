from flask import Blueprint, jsonify, request, session

r_general = Blueprint('r_general', __name__)

@r_general.route('/')
def home():
    return 'HOme Page'

@r_general.route('/logout')
def logout():
    session.clear()
    return {'message':'Exit'}

@r_general.route('/login', methods=['POST'])
def login():
    import app
    body = request.get_json()
    email = body['email']
    c_password = body['password']
    customer = app.customers_service.login(email, c_password)
    store = app.stores_service.login(email, c_password)
    if store:
        store = app.stores_service.get_store_by_email(email)
        token = app.create_token(
            store['id'], store['name'], app.secret_key)
        app.login_store(token, email)
        return token
    elif customer:
        customer = app.customers_service.get_customer_by_email(email)
        token = app.create_token(
            customer['id'], customer['name'], app.secret_key)
        app.login_customer(token, email)
        return token
    else:
        return 'Pleasse check your information'
