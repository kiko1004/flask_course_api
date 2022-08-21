from marshmallow import (
    Schema,
    fields,
    ValidationError,
    validate,
    validates_schema,
)
from password_strength import PasswordPolicy


class UserSingUpSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    phone = fields.String(required=False)
    password = fields.String(
        required=True, validate=validate.And(validate.Length(min=8, max=20))
    )

    @validates_schema
    def validate_data(self, data, **kwargs):
        if len(data["email"]) < 3:
            raise ValidationError("Email must be more than 3 characters", "email")
        if len(data["first_name"]) < 3:
            raise ValidationError("First name must be more than 3 characters", "email")
        if len(data["last_name"]) < 3:
            raise ValidationError("Last name must be more than 3 characters", "email")
        errors = PasswordPolicy.from_names(uppercase=1).test(data["password"])
        if errors:
            raise ValidationError("Not a valid password. {}".format(errors))


class LoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)
