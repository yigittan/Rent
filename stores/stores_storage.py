from bson.objectid import ObjectId

class StoreMongoStorage:
    def __init__(self,client):
        self.db = client.db.stores

    def insert(self,store):
        res = self.db.insert_one({
            "name":store.name,
            "city":store.city,
            "cars":store.cars,
            "email":store.email,
            "password":store.password
        })
        return str(res.inserted_id)

    def get_store_by_email(self,email):
        store = self.db.find_one({'email':email})
        if store is not None:
            return {
                'id':str(store['_id']),
                'name':store['name'],
                "cars":store['cars'],
                "password":store['password']
            }
        return None

    def get_store_by_id(self,store_id):
        store = self.db.find_one({'_id':ObjectId(store_id)})
        return {
            'name':store['name'],
            'city':store['city'],
            'cars':store['cars']
        }

    def add_car(self,car,store_id,car_id):
        self.db.update_one({'_id':ObjectId(store_id)} , {'$push': {'cars':car_id}})
        store = self.db.find_one({'_id':ObjectId(store_id)})
        return {
            'cars':store['cars']
        }

    def update_car(self,car,store_id,car_id):
        stores = self.db.find()
        for store in stores:
            print(store['cars'])
        return 'done'

    def delete_car(self,store_id,car_id):
        self.db.update_one({'_id':ObjectId(store_id)} , {'$pull': {'cars':car_id}})
        return car_id
