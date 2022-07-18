from functionalities import Recommender
from flask_restful import Resource
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import AnalystsModel
from schemas import *


class Recommendation(Resource):
    def get(self):
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
