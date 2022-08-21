from flask import request
from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource
from werkzeug.exceptions import Forbidden

from db import db
from functionalities import Recommender
from models import AnalystsModel, AnalysisModel, AnalysisType
from schemas import *

auth = HTTPTokenAuth(scheme="Bearer")


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
                raise Forbidden("Permission denied!")
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
            recommender = Recommender(data["ticker"])
            try:
                recommender.get_recomendation()
                params = {
                    "analyst_id": curr_user.id,
                    "ticker": data["ticker"],
                    "type": AnalysisType.recommendation.name,
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
    @permission_required("Premium")
    def get(self):
        curr_user = auth.current_user()
        data = request.args.to_dict()
        schema = Ticker()
        errors = schema.validate(data)
        if not errors:
            recommender = Recommender(data["ticker"])
            try:
                recommender.get_balancesheet()
                params = {
                    "analyst_id": curr_user.id,
                    "ticker": data["ticker"],
                    "type": AnalysisType.balance_sheet.name,
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
    @permission_required("Premium")
    def get(self):
        curr_user = auth.current_user()
        data = request.args.to_dict()
        schema = Ticker()
        errors = schema.validate(data)
        if not errors:
            recommender = Recommender(data["ticker"])
            try:
                recommender.get_analysis()
                params = {
                    "analyst_id": curr_user.id,
                    "ticker": data["ticker"],
                    "type": AnalysisType.analysis.name,
                }
                analysis = AnalysisModel(**params)
                db.session.add(analysis)
                db.session.commit()
                return recommender.res, 200
            except:
                return "Wrong ticker", 400
        return errors, 400


class ViewMyAnalysis(Resource):
    @auth.login_required
    def get(self):
        curr_user = auth.current_user()
        data = AnalysisModel.query.filter_by(analyst_id=curr_user.id).all()
        data = [i.as_dict() for i in data]
        response = []
        for entry in data:
            entry["type"] = entry["type"].name
            entry["created_on"] = entry["created_on"].strftime("%Y-%m-%d")
            del entry["updated_on"]
            response.append(entry)
        return response, 200
