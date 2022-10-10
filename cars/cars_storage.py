from bson.objectid import ObjectId

class CarMongoStorage:
    def __init__(self,client):
        self.db = client.db.cars

    def insert(self,car):
        res = self.db.insert_one({
            'name':car.name,
            "brand":car.brand,
            "color":car.color,
            "model_year":car.model_year,
            "price":car.price,
            "store_id":car.store_id,
            "km":car.km,
            "city":car.city,
            "rent":car.rent
        })
        return str(res.inserted_id)

    def update_car(self,car,car_id):
        self.db.update_one({'_id':ObjectId(car_id)} , {'$set': {'name':car.name , 'brand':car.brand, 'color':car.color, 'model_year':car.model_year, 'price':car.price, 'store_id':car.store_id, 'km':car.km, 'city':car.city,'rent':car.rent}})
        return car_id

    def delete_car(self,car_id):
        self.db.delete_one({'_id':ObjectId(car_id)})
        return car_id

    def filter(self,search_query):
        cars = self.db.find(search_query)
        return [{
            "name":car['name'],
            "brand":car['brand'],
            "color":car['color'],
            "model_year":car['model_year'],
            "price":car['price'],
            'store_id':car['store_id'],
            "km":car['km'],
            "city":car['city'],
            "rent":car['rent']
        }for car in cars]