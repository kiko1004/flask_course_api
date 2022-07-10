from sqlalchemy import func

from db import db
from models.enums import ComplaintState


class AnalysisModel(db.Model):
    __tablename__ = 'analysis'
    id = db.Column(db.Integer, primary_key=True)
    analyst_id = db.Column(db.Integer, db.ForeignKey("analysts.id"), nullable=False)
    ticker = db.Column(db.String(30), nullable=False)
    outcome = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.String(20), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_on = db.Column(db.DateTime, onupdate=func.now())
    complainer = db.relationship("AnalystsModel")
