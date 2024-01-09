import json
from unittest.mock import patch

import aiohttp
import pytest


class TestBookViews:

    async def test_get_book_list(self, test_client, add_books):
        response = await test_client.post('/books/', json={})
        assert response.status == 200
        data = await response.json()

        assert isinstance(data, dict)
        assert len(data['items']) == 3

    @pytest.mark.parametrize('request_body, result',
                             [
                                 ({'filter_name': ['book1']}, 1),
                                 ({'filter_name': ['book1', 'book2']}, 2),
                                 ({'filter_author': ['author3']}, 1),
                                 ({'date_start': '01.01.2024', 'date_end': '01.01.2024'}, 1),
                                 ({'query': '1'}, 1),
                             ])
    async def test_get_book_list_filter(self, test_client, add_books, request_body, result):
        response = await test_client.post('/books/',
                                          json=request_body)
        assert response.status == 200
        data = await response.json()

        assert isinstance(data, dict)
        assert len(data['items']) == result

    @pytest.mark.parametrize('request_body, result',
                             [
                                 ({'sort': 'name'}, (3, 2)),
                                 ({'sort': 'name', 'sort_order': 'asc'}, (1, 2)),
                                 ({'sort': 'author', 'sort_order': 'desc'}, (3, 2)),
                                 ({'sort': 'date_published', 'sort_order': 'asc'}, (1, 2)),
                             ])
    async def test_get_book_list_sort(self, test_client, add_books, request_body, result):
        response = await test_client.post('/books/',
                                          json=request_body)
        assert response.status == 200
        data = await response.json()

        assert isinstance(data, dict)
        assert data['items'][0]['id'] == result[0]
        assert data['items'][1]['id'] == result[1]

    @pytest.mark.parametrize('request_body',
                             [
                                 ({'sort': 'not_exist_column'}),
                             ])
    async def test_get_book_list_sort_error(self, test_client, add_books, request_body):
        response = await test_client.post('/books/',
                                          json=request_body)
        assert response.status == 422

    async def test_get_book(self, test_client, add_books):
        response = await test_client.get('/books/1/')
        assert response.status == 200
        data = await response.json()

        assert isinstance(data, dict)
        assert data == {'id': 1, 'name': 'book1', 'author': 'author1',
                        'date_published': '01.01.2024', 'genre': 'fantasy'}

    async def test_get_book_not_found(self, test_client):
        response = await test_client.get('/books/99/')
        assert response.status == 404

    async def test_get_book_error(self, test_client):
        response = await test_client.get('/books/invalid_id/')
        assert response.status == 422

    async def test_create_book(self, test_client):
        file = b'test_content'
        metadata = {
            'name': 'Test Book',
            'author': 'Test Author',
            'date_published': '01.01.2024'
        }

        data = aiohttp.FormData()
        data.add_field('file',
                       file,
                       filename='report.pdf',
                       content_type='application/pdf')
        data.add_field('data',
                       json.dumps(metadata),
                       content_type='application/json')
        response = await test_client.post('/books/upload/', data=data)
        assert response.status == 201
        data = await response.json()
        assert 'book_id' in data

    @pytest.mark.parametrize('request_data',
                             [
                                 ({'name': '',
                                   'author': 'Test Author',
                                   'date_published': '01.01.2024'}),
                                 ({'name': 'Test Book',
                                   'author': '',
                                   'date_published': '01.01.2024'}),
                                 ({'name': 'Test Book',
                                   'author': 'Test Author',
                                   'date_published': ''}),
                                 ({'name': 'Test Book',
                                   'author': 'Test Author'}),
                             ])
    async def test_create_book_error(self, test_client, request_data):
        file = b'test_content'
        metadata = request_data

        data = aiohttp.FormData()
        data.add_field('file',
                       file,
                       filename='report.pdf',
                       content_type='application/pdf')
        data.add_field('data',
                       json.dumps(metadata),
                       content_type='application/json')
        response = await test_client.post('/books/upload/', data=data)
        assert response.status == 422

    async def test_create_book_bad_request(self, test_client):
        file = b'test_content'

        data = aiohttp.FormData()
        data.add_field('file',
                       file,
                       filename='report.csv',
                       content_type='application/csv')
        response = await test_client.post('/books/upload/', data=data)
        assert response.status == 400

    @patch('apps.books.utils.download_file')
    async def test_download_book(self, download_file_mock, test_client):
        download_file_mock.return_value = b'text data'

        response = await test_client.get('/books/1/download/')
        assert response.status == 200
