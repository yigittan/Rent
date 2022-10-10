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
        
    