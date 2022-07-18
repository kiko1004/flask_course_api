from functionalities import Recommender
from flask_restful import Resource, abort
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import AnalystsModel
from schemas import *
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(token):
    try:
        user_id = AnalystsModel.decode_token(token=token)
        return AnalystsModel.query.filter_by(id=user_id).first()
    except:
        return False

def permission_required(permission):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            user = auth.current_user()
            if not user.role == permission:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


class Recommendation(Resource):
    @auth.login_required
    def get(self):
        curr_user = auth.current_user()
        data = request.args.to_dict()
        schema = Ticker()
        errors = schema.validate(data)
        if not errors:
            recommender = Recommender(data['ticker'])
            try:
                recommender.get_recomendation()
                return recommender.res, 200
            except:
                return "Wrong ticker", 400
        return errors, 400
