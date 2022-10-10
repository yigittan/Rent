class CarService:
    def __init__(self,storage):
        self.storage = storage

    def create(self,car):
        return self.storage.insert(car)

    def update_car(self,car,car_id):
        return self.storage.update_car(car,car_id)

    def delete_car(self,car_id):
        return self.storage.delete_car(car_id)

    def filter(self,search_query):
        return self.storage.filter(search_query)
