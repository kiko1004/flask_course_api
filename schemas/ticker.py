from marshmallow import (
    Schema,
    fields,
)


class Ticker(Schema):
    ticker = fields.String(required=True)
