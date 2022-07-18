from sqlalchemy import func

from db import db
from models.enums import *


class AnalysisModel(db.Model):
    __tablename__ = 'analysis'
    id = db.Column(db.Integer, primary_key=True)
    analyst_id = db.Column(db.Integer, db.ForeignKey("analysts.id"), nullable=False)
    ticker = db.Column(db.String(30), nullable=False)
    type = db.Column(db.Enum(AnalysisType), server_default=AnalysisType.analysis.name, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_on = db.Column(db.DateTime, onupdate=func.now())
    relationship = db.relationship("AnalystsModel")
