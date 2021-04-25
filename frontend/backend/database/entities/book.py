from umongo import Document, MotorAsyncIOInstance
from umongo.fields import StringField, ListField, IntegerField

from server import app

instance: MotorAsyncIOInstance = app.config["LAZY_UMONGO"]


@instance.register
class Book(Document):
    model_id = IntegerField(required=True, allow_none=False, unique=True)
    picture = StringField(required=False, allow_none=True, default="")
    title = StringField(required=True, allow_none=False)
    author = StringField(required=False, allow_none=False, default="")
    published_date = StringField(required=False, allow_none=True, default="")
    description = StringField(required=False, allow_none=True, default="")
    genre = StringField(required=False, allow_none=True, default="")
    tags = ListField(StringField(required=False, allow_none=True), default=[])

    def get_info(self):
        data = {
            "title": self.title,
            "metatype": "Book",
            "type": self.genre,
            "picture": self.picture,
            "description": self.description,
            "additional": [
                {
                    "title": "author",
                    "data": self.author
                },
                {
                    "title": "published_date",
                    "data": self.published_date
                }
            ],
            "tags": self.tags
        }
        return data
