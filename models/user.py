from sqlalchemy import func

from db import db
from models.enums import UserRole


class BaseUserModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    phone = db.Column(db.String(14), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_on = db.Column(db.DateTime, onupdate=func.now())


class AnalystsModel(BaseUserModel):
    __tablename__ = 'analysts'
    complaints = db.relationship("AnalysisModel", backref="analysis", lazy='dynamic')
    role = db.Column(db.Enum(UserRole), default=UserRole.Basic, nullable=False)


class AdminModel(BaseUserModel):
    __tablename__ = 'admins'
    role = db.Column(db.Enum(UserRole), default=UserRole.admin, nullable=False)
