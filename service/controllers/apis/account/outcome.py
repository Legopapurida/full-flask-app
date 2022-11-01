from marshmallow import Schema
from marshmallow import fields


class AddUserSchema(Schema):
    username = fields.Str()
