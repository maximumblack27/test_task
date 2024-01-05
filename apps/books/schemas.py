from marshmallow import Schema, fields

from apps.books.models import BookModel
from config.settings import DATETIME_FORMAT


class BookSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    author = fields.String()
    date_published = fields.DateTime(format=DATETIME_FORMAT)
    genre = fields.String()

    class Meta:
        model = BookModel
