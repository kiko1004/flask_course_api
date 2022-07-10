from marshmallow import Schema, fields, validates, ValidationError, validate, validates_schema


class UserSingUpSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    phone = fields.String(required=False)
    password = fields.String(required=True, validate=validate.And(validate.Length(min=8, max=20)))

    @validates_schema
    def validate_email(self, data, **kwargs):
        if len(data['email']) < 3:
            raise ValidationError('Email must be more than 3 characters', 'email')
        if len(data['first_name']) < 3:
            raise ValidationError('First name must be more than 3 characters', 'email')
        if len(data['last_name']) < 3:
            raise ValidationError('Last name must be more than 3 characters', 'email')