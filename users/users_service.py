from flask import Flask, jsonify

class UserService:
    def __init__(self,storage):
        self.storage = storage

    def create(self,user):
        return self.storage.insert(user)

    def login(self,email,c_password):
        user = self.storage.get_user_by_email(email)
        if c_password == user['password']:
            return True
        else:
            return False

    def get_user_by_email(self,email):
        return self.storage.get_user_by_email(email)

    def get_user_by_id(self,user_id):
        return self.storage.get_user_by_id(user_id)