from datetime import datetime, timedelta

import jwt
from decouple import config
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy import func
from werkzeug.exceptions import Unauthorized

from db import db
from models.enums import UserRole


class BaseUserModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    phone = db.Column(db.String(14), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_on = db.Column(db.DateTime, onupdate=func.now())


class AnalystsModel(BaseUserModel):
    __tablename__ = "analysts"
    analysis = db.relationship("AnalysisModel", backref="analysis", lazy="dynamic")
    role = db.Column(db.Enum(UserRole), default=UserRole.Basic, nullable=False)

    def encode_token(self):
        try:
            payload = {"exp": datetime.utcnow() + timedelta(days=2), "sub": self.id}
            return jwt.encode(payload, key=config("SECRET_KEY"), algorithm="HS256")
        except Exception as e:
            raise e

    @staticmethod
    def decode_token(token):
        if not token:
            raise Unauthorized("Missing token")
        try:
            payload = jwt.decode(token, key=config("SECRET_KEY"), algorithms=["HS256"])
            return payload["sub"]
        except ExpiredSignatureError:
            raise Unauthorized("Token expired")
        except InvalidTokenError:
            raise Unauthorized("Invalid token")


class AdminModel(BaseUserModel):
    __tablename__ = "admins"
    role = db.Column(db.Enum(UserRole), default=UserRole.admin, nullable=False)
