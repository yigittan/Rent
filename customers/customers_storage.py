class CustomerMongoStorage:
    def __init__(self,client):
        self.db = client.db.customers

    def insert(self,customer):
        res = self.db.insert_one({
            'name':customer.name,
            'surname':customer.surname,
            'username':customer.username,
            'email':customer.email,
            'password':customer.password,
            'city':customer.city
        })
        return str(res.inserted_id)

    def get_customer_by_email(self,email):
        customer = self.db.find_one({'email':email})
        if customer is not None:
            return {
                "id": str(customer['_id']),
                "name":customer['name'],
                "username":customer['username'],
                "password":customer['password']
            }
        return None