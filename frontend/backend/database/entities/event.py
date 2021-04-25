from umongo import Document, MotorAsyncIOInstance
from umongo.fields import StringField, ListField, IntegerField

from server import app

instance: MotorAsyncIOInstance = app.config["LAZY_UMONGO"]


@instance.register
class Event(Document):
    model_id = IntegerField(required=True, allow_none=False, unique=True)
    picture = StringField(required=False, allow_none=True, default="")
    title = StringField(required=True, allow_none=False)
    author = StringField(required=True, allow_none=False)
    date = StringField(required=False, allow_none=True, default="")
    location = StringField(required=False, allow_none=True, default="")
    description = StringField(required=False, allow_none=True, default="")
    genre = StringField(required=False, allow_none=True, default="")
    tags = ListField(StringField(required=False, allow_none=True), default=[])

    def get_info(self):
        data = {
            "title": self.title,
            "metatype": "Event",
            "type": self.genre,
            "picture": self.picture,
            "description": self.description,
            "additional": [
                {
                    "title": "date",
                    "data": self.date
                },
                {
                    "title": "location",
                    "data": self.location
                },
                {
                    "title": "author",
                    "data": self.author
                }
            ],
            "tags": self.tags
        }
        return data
