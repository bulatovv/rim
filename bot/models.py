from tortoise.models import Model
from tortoise import fields

class User(Model):
    fullname = fields.CharField(max_length=64)
    score = fields.IntField(default=0)
