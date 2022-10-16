from bson.objectid import ObjectId


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
            'city':customer.city,
            "wallet":customer.wallet,
            "rented_cars":customer.rented_cars
        })
        return str(res.inserted_id)

    def get_customer_by_email(self,email):
        customer = self.db.find_one({'email':email})
        if customer is not None:
            return {
                "id": str(customer['_id']),
                "name":customer['name'],
                "username":customer['username'],
                "password":customer['password'],
                "customer":customer['email'],
                "wallet":customer['wallet'],
                "rented_cars":customer['rented_cars']
            }
        return None

    def update_wallet_for_rent(self,customer,wallet,car_id):
        customer_id = customer['id']
        self.db.update_one({'_id':ObjectId(customer_id)}, {'$set': {'wallet':wallet }})
        res = self.db.update_one({'_id':ObjectId(customer_id)} , {'$push': {'rented_cars':car_id}})
        return wallet

    def get_all_customers(self):
        customers = self.db.find()
        return [{
            "id": str(customer['_id']),
                "name":customer['name'],
                "username":customer['username'],
                "password":customer['password'],
                "customer":customer['email'],
                "wallet":customer['wallet'],
                "rented_cars":customer['rented_cars']
        }for customer in customers]

    def update_wallet(self,customer,wallet,car_id):
        self.db.update_one({'_id':ObjectId(customer['id'])}, {'$set': {'wallet':wallet}})
        self.db.update_one({'_id':ObjectId(customer['id'])}, {'$pull': {'rented_cars':car_id}})
        return customer['id']