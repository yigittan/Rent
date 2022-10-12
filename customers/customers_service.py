class CustomerService:
    def __init__(self,storage):
        self.storage = storage

    def create(self,customer):
        return self.storage.insert(customer)

    def login(self,email,c_password):
        customer =  self.storage.get_customer_by_email(email)
        if customer is not None:
            if c_password == customer['password']:
                return True
            else:
                return False
        return False

    def get_customer_by_email(self,email):
        return self.storage.get_customer_by_email(email)

    def is_available(self,car,customer):
        wallet = customer['wallet']
        car_id = car['id']
        price = car['price']
        if wallet >= price and car['rent'] == "available":
            wallet -= price
            self.storage.update_wallet_for_rent(customer,wallet,car_id)
            return True
        return False

    def get_all_customers(self,car_id):
        customers = self.storage.get_all_customers()
        for customer in customers:
            if car_id in customer['rented_cars']:
                return customer
            
    def pay_back(self,customer,car):
        wallet = customer['wallet']
        price = car['price']
        wallet +=price
        return self.storage.update_wallet(customer,wallet)
            
            