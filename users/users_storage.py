from bson.objectid import ObjectId

class UserMongoStorage:
    def __init__(self,client):
        self.db = client.db.users

    def insert(self,user):
        res = self.db.insert_one({
            'name':user.name,
            "surname":user.surname,
            "username":user.username,
            "email":user.email,
            "password":user.password,
            "city":user.city,
            "role":user.role
        })
        return str(res.inserted_id)

    def get_user_by_email(self,email):
        user = self.db.find_one({'email':email})
        print(user)
        if user is None:
            return None
        return {
            "id":str(user['_id']),
            "name":user['name'],
            "surname":user['surname'],
            "username":user['username'],
            "password":user['password']
        }
        