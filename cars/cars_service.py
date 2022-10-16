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

    def rent(self,car_id):
        return self.storage.rent(car_id)

    def get_car_by_id(self,car_id):
        return self.storage.get_car_by_id(car_id)

    def get_all_car_by_id(self,store_id):
        return self.storage.get_all_car_by_id(store_id)

    def cancel_car(self,car_id):
        car = self.storage.get_car_by_id(car_id)
        if car['rent'] == 'Already Rented':
            return True
        else:
            return False
        
    def update_car_rent(self,car_id):
        return self.storage.update_car_rent(car_id)