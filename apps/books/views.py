import json

from aiohttp import BodyPartReader, web

from apps.books.managers import BookFileManager, BookManager
from apps.books.schemas import (BookFileSchema, BookQuerySchema, BookSchema,
                                CreateBookSchema, LoadingFileSchema,
                                PageParamsSchema)
from apps.books.utils import (download_file, extract_query_param, get_value_from_request,
                              save_file, read_pdf_from_page)
from config import settings

book_routes = web.RouteTableDef()


@book_routes.post('/books/')
async def get_book_list(request: web.Request) -> web.Response:
    """
    Handler for retrieving a list of books based on specified filters and pagination.
    Handler is used POST method for exclude errors related on delimiters in a filters.

    Request JSON Payload:
    {
        "filter_name": List of strings (optional) - Filter books by name,
        "filter_author": List of strings (optional) - Filter books by author,
        "date_start": Date string (optional) - Filter books published on or after this date,
        "date_end": Date string (optional) - Filter books published on or before this date,
        "filter_genre": List of strings (optional) - Filter books by genre,
        "query_string": String (optional) - Full-text search query,
        "sort": String (optional) - Column to sort the result by (e.g., "name", "author"),
        "sort_order": String (optional) - Sort order ("asc" or "desc")
        "page_number": Integer (optional) - Page number for pagination,
        "page_size": Integer (optional) - Number of items per page (default: settings.MAX_PAGE_SIZE)
    }

    Returns:
    {
        "page": Integer - Current page number,
        "items": List of dictionaries - Book information,
    }
    """
    request_data = await request.read()

    args = BookQuerySchema().load(json.loads(request_data)) if request_data else {}
    page_params = {
        'page_number': extract_query_param(request, 'page_number', int, 1),
        'page_size': extract_query_param(request, 'page_size', int, settings.MAX_PAGE_SIZE)
    }
    args.update(PageParamsSchema().load(page_params))

    schema = BookSchema()
    books = await BookManager.get_book_list(**args)
    data = schema.dump(books, many=True)
    response_data = {
        'page': page_params['page_number'],
        'items': data
    }

    return web.Response(
        body=json.dumps(response_data, ensure_ascii=False).encode('utf8'),
        status=200,
        content_type='application/json'
    )


@book_routes.get('/books/{book_id}/')
async def get_book(request: web.Request) -> web.Response:
    """
    Handler for retrieving details of a specific book.

    Path Parameter:
    - book_id: Integer - Unique identifier for the book.

    Returns:
    {
        "id": Integer - Book ID,
        "name": String - Book name,
        "author": String - Author of the book,
        "published_date": String - Published date of the book (format: DD.MM.YYYY),
        "genre": String - Genre of the book
    }
    """
    book_id = get_value_from_request(request, 'book_id')

    schema = BookSchema()
    book = await BookManager.get_book(book_id=book_id)
    data = schema.dump(book)

    return web.Response(
        body=json.dumps(data, ensure_ascii=False).encode('utf8'),
        status=200,
        content_type='application/json'
    )


@book_routes.post('/books/upload/')
async def upload_book(request: web.Request) -> web.json_response:
    """
    Handler for uploading a new book along with associated files.

    Request Format:
    - Method: POST
    - Endpoint: '/books/upload/'
    - Headers:
        Content-Type: multipart/form-data
    - Body:
        - 'file': Binary - The book file to be uploaded.
        - 'data': JSON - Additional data for creating the book.
            {
                "name": String - Book name,
                "author": String - Author of the book,
                "genre": String - Genre of the book,
                "published_date": String - Published date of the book (format: DD.MM.YYYY),
                ... (other fields for book details)
            }

    Example cURL Command:
    ```bash
    curl -X POST 'http://localhost:8000/books/upload/' \
         -F 'file=@{path_to_file}' \
         -F 'data={"name":"book name","author":"book author","date_published":"01.01.2024"}'
    ```

    Returns:
    {
        "book_id": Integer - Unique identifier for the uploaded book.
    }
    """
    reader = await request.multipart()
    field: BodyPartReader = await reader.next()

    file_schema = LoadingFileSchema()
    file_schema.load({'file_headers': field.headers})

    file_name = await save_file(field)

    request_data = await request.post()
    request_data = json.loads(request_data.get('data'))

    schema = CreateBookSchema()
    args = schema.load(request_data)

    manager = BookManager()
    await manager.add_book(**args)

    file_manager = BookFileManager()
    await file_manager.add_book_file(
        book_id=manager.instance.id, file_name=file_name, origin_file_name=field.filename
    )

    return web.json_response(data={"book_id": manager.instance.id}, status=201)


@book_routes.get('/books/{book_id}/download/')
async def download_book(request: web.Request) -> web.StreamResponse:
    """
    Handler for downloading the file associated with a book.

    Returns:
    - Content-Disposition: attachment;filename={file_name}
    - Content-Type: multipart/x-mixed-replace
    - File content: The binary content of the book file.
    """
    book_id = get_value_from_request(request, 'book_id')

    schema = BookFileSchema()
    book = await BookFileManager.get_file_name(book_id=book_id)
    file = schema.dump(book)

    response = web.StreamResponse(
        status=200,
        reason='OK',
        headers={
            'Content-Type': 'multipart/x-mixed-replace',
            'CONTENT-DISPOSITION': f'attachment;filename={file.get("name")}'
        }
    )
    await response.prepare(request)

    return await download_file(response, file)


@book_routes.get('/books/{book_id}/read/{page_number}/')
async def view_pdf_page(request: web.Request) -> web.Response:
    """
    Handler for retrieving a specific page of a book in PDF format.

    Path Parameters:
    - book_id: Integer - Unique identifier for the book.
    - page_number: Integer - Page number of the book to be retrieved.

    Returns:
    - Content-Type: image/png
    - File content: Binary data representing the specified page of the book in PNG format.
    """
    book_id = get_value_from_request(request, 'book_id')
    page_number = get_value_from_request(request, 'page_number')

    schema = BookFileSchema()
    book = await BookFileManager.get_file_name(book_id=book_id)
    file = schema.dump(book)

    image_bytes = read_pdf_from_page(file, page_number)

    return web.Response(
        body=image_bytes,
        content_type='image/png'
    )
