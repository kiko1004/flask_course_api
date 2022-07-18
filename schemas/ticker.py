from marshmallow import Schema, fields, validates, ValidationError, validate, validates_schema

class Ticker(Schema):
    ticker = fields.String(required=True)
