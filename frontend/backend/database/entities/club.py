from umongo import Document, MotorAsyncIOInstance
from umongo.fields import StringField, ListField, IntegerField

from server import app

instance: MotorAsyncIOInstance = app.config["LAZY_UMONGO"]


@instance.register
class Club(Document):
    model_id = IntegerField(required=True, allow_none=False, unique=True)
    picture = StringField(required=False, allow_none=True, default="")
    title = StringField(required=True, allow_none=False)
    description = StringField(required=False, allow_none=True, default="")
    genre = StringField(required=False, allow_none=True, default="")
    tags = ListField(StringField(required=False, allow_none=True), default=[])

    def get_info(self):
        data = {
            "title": self.title,
            "metatype": "Club",
            "type": self.genre,
            "picture": self.picture,
            "description": self.description,
            "additional": [],
            "tags": self.tags
        }
        return data
