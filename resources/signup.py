from flask_restful import Resource
from flask import request
from werkzeug.security import generate_password_hash
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
            token = user.encode_token()
            db.session.add(user)
            db.session.commit()
            return {'token': token}, 201
        return errors
