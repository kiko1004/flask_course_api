from functionalities import Recommender
from flask_restful import Resource, abort
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import AnalystsModel, AnalysisModel
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
            if not user.role.name == permission:
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
                params = {
                    'analyst_id': curr_user.id,
                    'ticker': data['ticker'],
                    'type': 'recommendation',
                }
                analysis = AnalysisModel(**params)
                db.session.add(analysis)
                db.session.commit()
                return recommender.res, 200
            except:
                return "Wrong ticker", 400
        return errors, 400


class BalanceSheet(Resource):
    @auth.login_required
    @permission_required('Premium')
    def get(self):
        curr_user = auth.current_user()
        data = request.args.to_dict()
        schema = Ticker()
        errors = schema.validate(data)
        if not errors:
            recommender = Recommender(data['ticker'])
            try:
                recommender.get_balancesheet()
                params = {
                    'analyst_id': curr_user.id,
                    'ticker': data['ticker'],
                    'type': 'balance sheet',
                }
                analysis = AnalysisModel(**params)
                db.session.add(analysis)
                db.session.commit()
                return recommender.res, 200
            except:
                return "Wrong ticker", 400
        return errors, 400

class Analysis(Resource):
    @auth.login_required
    @permission_required('Premium')
    def get(self):
        curr_user = auth.current_user()
        data = request.args.to_dict()
        schema = Ticker()
        errors = schema.validate(data)
        if not errors:
            recommender = Recommender(data['ticker'])
            try:
                recommender.get_analysis()
                params = {
                    'analyst_id': curr_user.id,
                    'ticker': data['ticker'],
                    'type': 'analysis',
                }
                analysis = AnalysisModel(**params)
                db.session.add(analysis)
                db.session.commit()
                return recommender.res, 200
            except:
                return "Wrong ticker", 400
        return errors, 400