from flask import Flask, jsonify
from app import jwt
class UserService:
    def __init__(self,storage):
        self.storage = storage

    def create(self,user):
        return self.storage.insert(user)

    def login(self,email,c_password):
        user = self.storage.get_user_by_email(email)
        if user is None:
            return {'message':'user not found'}
        if c_password == user['password']:
            return user
        else:
            return {'message':'please check your password'}