class CarService:
    def __init__(self,storage):
        self.storage = storage

    def create(self,car):
        return self.storage.insert(car)

    def car_by_id(self,car_id):
        res = self.storage.get_by_id(car_id)
        return res

    def filter(self,filter_query):
        return self.storage.get_by_filter(filter_query)
    
    