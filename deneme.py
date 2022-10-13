#r_store dosyası
from flask import Blueprint, request

r_store = Blueprint('r_store',__name__)


@r_store.route('/<string:store_id>' , methods=['POST'])
def store(store_id):
    if request.method == 'POST':
        return store_id


#APP dosyası

from flask import Flask

# import r_store

r_store.register_blueprint(r_store,prefix_url='/store')

@r_store.route('/<string:store_id>' , methods=['POST'])
def store_id(store_id):
    return 'Something Else'


# r_store dosyasındaki ve app dosyasındaki route aynı
#app den çalıştırdığımızda return etmesi gereken 'Something else' gelmiyor
# app den çalışınca direk olarak r_store daki routeun fonksiyonun returnü geliyor