from marshmallow import Schema, fields, validates_schema

from apps.books.models import BookModel
from config.settings import DATETIME_FORMAT, DATE_FORMAT


class BookSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    author = fields.String()
    date_published = fields.DateTime(format=DATETIME_FORMAT)
    genre = fields.String()

    class Meta:
        model = BookModel


class PageParamsSchema(Schema):
    page_number = fields.Int()
    page_size = fields.Int()

    @validates_schema
    def validate_schema(self, data, *args, **kwargs):
        data['page_number'] = data['page_number'] - 1

        return data


class BookQuerySchema(Schema):
    filter_name = fields.List(fields.Str, missing=None)
    filter_author = fields.List(fields.Str, missing=None)
    date_start = fields.Date(format=DATE_FORMAT, missing=None)
    date_end = fields.Date(format=DATE_FORMAT, missing=None)
    filter_genre = fields.List(fields.Str, missing=None)
