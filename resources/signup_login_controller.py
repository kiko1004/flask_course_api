from flask_restful import Resource
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import AnalystsModel


from schemas import *


class SignUp(Resource):
    def post(self):
        data = request.get_json()
        schema = UserSingUpSchema()
        errors = schema.validate(data)
        if not errors:
            data["password"] = generate_password_hash(data['password'], method='sha256')
            user = AnalystsModel(**data)
            db.session.add(user)
            db.session.commit()
            user = AnalystsModel.query.filter_by(email=user.email).first()
            token = user.encode_token()
            return {'token': token}, 201
        return errors


class Login(Resource):
    def post(self):
        data = request.get_json()
        schema = LoginSchema()
        errors = schema.validate(data)
        if not errors:
            user = AnalystsModel.query.filter_by(email=data['email']).first()
            logged_in = check_password_hash(user.password, data['password'])
            if logged_in:
                token = user.encode_token()
                return {'token': token}, 200
            else:
                return 'Wrong email or password', 401
        return errors
