from datetime import datetime

books = [
    {
        'id': 1,
        'name': 'book1',
        'author': 'author1',
        'date_published': datetime(2024, 1, 1).date(),
        'genre': 'fantasy'
    },
    {
        'id': 2,
        'name': 'book2',
        'author': 'author2',
        'date_published': datetime(2024, 1, 2).date(),
        'genre': 'scientific'
    },
    {
        'id': 3,
        'name': 'book3',
        'author': 'author3',
        'date_published': datetime(2024, 1, 3).date(),
        'genre': 'sci-fi',
    }
]

book_files = [
    {
        'id': 1,
        'book_id': 1,
        'file_name': 'filename1.pdf',
        'origin_file_name': 'originfilename1.pdf',
        'text': None
    },
    {
        'id': 2,
        'book_id': 2,
        'file_name': 'filename2.pdf',
        'origin_file_name': 'originfilename2.pdf',
        'text': None
    },
    {
        'id': 3,
        'book_id': 3,
        'file_name': 'filename3.pdf',
        'origin_file_name': 'originfilename3.pdf',
        'text': None
    }
]
