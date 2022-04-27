from flask import Blueprint, request, redirect
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal_with
from app.models import User, UserData, db
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
auth = Api(auth_bp)

class Login(Resource):
    def get(self):
        return {"msg": "login get"}
    def post(self):
        return {"msg": "login post"}

class Logout(Resource):
    def get(self):
        return {"msg": "logout get"}
    def post(self):
        return {"msg": "logout post"}


auth.add_resource(Login, "/login")
auth.add_resource(Logout, "/logout")
