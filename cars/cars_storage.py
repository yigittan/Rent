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


    def rent(self,car_id):
        self.db.update_one({'_id':ObjectId(car_id)},{'$set':{'rent':'Already Rented'}})
        car = self.db.find_one({'_id':ObjectId(car_id)})
        return car['rent']    

    def get_car_by_id(self,car_id):
        car = self.db.find_one({'_id':ObjectId(car_id)})
        return {
            "name":car['name'],
            "brand":car['brand'],
            "color":car['color'],
            "model_year":car['model_year'],
            "price":car['price'],
            'store_id':car['store_id'],
            "km":car['km'],
            "city":car['city'],
            "rent":car['rent']
        }
        
    def get_all_car_by_id(self,store_id):
        print("BURADAYIM")
        cars = self.db.find({'store_id':store_id})
        print("BURADAYIM")
        return [{
            "id":str(car['_id']),
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