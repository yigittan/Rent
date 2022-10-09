class CarMongoStorage:
    def __init__(self,client):
        self.db = client.db.cars

    def insert(self,car):
        res = self.db.insert_one({
            "store_id":car.store_id,
            "name":car.name,
            "brand":car.brand,
            "price":car.price,
            "model_year":car.model_year,
            "color":car.color,
            "status":car.status,
            "km":car.km
        })

        return str(res.inserted_id)
    
    def get_by_id(self,car_id):
        car = self.db.find_one({'_id':car_id})
        if car is None:
            return None
        return {
            "id":str(car['id']),
            "store_id":car['store_id'], 
            "name":car['name'],
            "brand":car['brand'],
            "price":car['price'],
            "year":car['year'],
            "status":car['status'],
            "store":car['user_id']
        }

    def get_by_filter(self,filter_query):
        cars = self.db.find(filter_query)
        cars_array = [{
            "id":str(car['id']),
            "name":car['name'],
            "brand":car['brand'],
            "price":car['price'],
            "year":car['year'],
            "status":car['status'],
            "store_id":car['user_id'],
            "km":car['km'],
            "city":car['city']
        }for car in cars]

        return cars_array

    