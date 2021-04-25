from umongo import Document, MotorAsyncIOInstance
from umongo.fields import StringField, ListField, IntegerField

from server import app

instance: MotorAsyncIOInstance = app.config["LAZY_UMONGO"]


@instance.register
class User(Document):
    model_id = IntegerField(required=True, allow_none=False, unique=True)
    username = StringField(required=True, allow_none=False, unique=True)
    password = StringField(required=True, allow_none=False)
    salt = StringField(required=True, unique=True, allow_none=False)
    books = ListField(IntegerField(), default=[])
    clubs = ListField(IntegerField(), default=[])
    events = ListField(IntegerField(), default=[])
