from aiohttp.web_exceptions import HTTPUnprocessableEntity, HTTPNotFound
from marshmallow import Schema, fields, validates_schema, pre_dump
from marshmallow.validate import OneOf

from apps.books.enums import BookColumnEnum
from apps.books.models import BookModel, BookFileModel
from config.settings import DATE_FORMAT


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    author = fields.Str()
    date_published = fields.Date(format=DATE_FORMAT)
    genre = fields.Str()

    @pre_dump
    def pre_dump(self, data, *args, **kwargs):
        if not data:
            raise HTTPNotFound(reason='book not found')

        return data

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
    query_string = fields.Str(missing=None, data_key='query')
    sort = fields.Str(missing=None, validate=OneOf(choices=BookColumnEnum.get_values()))
    sort_order = fields.Str(missing=None, validate=OneOf(choices=['asc', 'desc', 'ASC', 'DESC']))


class CreateBookSchema(Schema):
    name = fields.Str()
    author = fields.Str()
    date_published = fields.Date(format=DATE_FORMAT)
    genre = fields.Str(missing=None)

    @validates_schema
    def validate_schema(self, data, *args, **kwargs):
        if not data.get('name') or not data.get('author') or not data.get('date_published'):
            raise HTTPUnprocessableEntity(reason='"name", "author" and "date_published" must be filled')

        return data


class BookFileSchema(Schema):
    name = fields.Str()
    file_name = fields.Str()

    @pre_dump
    def pre_dump(self, data, *args, **kwargs):
        if not data:
            raise HTTPNotFound(reason='book file not found')

        return data
