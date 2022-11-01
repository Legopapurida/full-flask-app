from marshmallow import Schema
from marshmallow import fields


class RegisterSchema(Schema):
    username = fields.Str()
