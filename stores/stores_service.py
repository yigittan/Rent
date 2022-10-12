class StoreService:
    def __init__(self,storage):
        self.storage = storage

    def create(self,store):
        return self.storage.insert(store)

    def login(self,email,c_password):
        store = self.storage.get_store_by_email(email)
        if store is not None:
            if c_password == store['password']:
                return True
            else:
                return False
        return False

    def get_store_by_email(self,email):
        store = self.storage.get_store_by_email(email)
        return store

    def get_store_by_id(self,store_id):
        return self.storage.get_store_by_id(store_id)

    def add_car(self,car,store_id,car_id):
        return self.storage.add_car(car,store_id,car_id)

    def update_car(self,car,store_id,car_id):
        return self.storage.update_car(car,store_id,car_id)

    def delete_car(self,store_id,car_id):
        return self.storage.delete_car(store_id,car_id)

    def payment_for_rent(self,car,store):
        store_wallet = store['store_wallet']
        payment = car['price']
        store_wallet +=payment
        store_id = car['store_id']
        return self.storage.update_store_wallet(store_wallet,store_id)