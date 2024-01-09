# Book Management API

The Book Management API is designed to manage books and associated files. It provides endpoints to retrieve a list of books, get details of a specific book, upload a new book along with its files, and download the associated file of a book.

## Endpoints

### 1. Retrieve a List of Books

- **Method:** POST
- **Endpoint:** `/books/`

Example cURL Command:
 ```bash
 curl -X POST 'http://localhost:8000/books/'
 ```

### 2. Retrieve Details of a Specific Book

- **Method:** GET
- **Endpoint:** `/books/{book_id}/`

Example cURL Command:
 ```bash
 curl -X GET 'http://localhost:8000/books/1/'
 ```

### 3. Upload a New Book

- **Method:** POST
- **Endpoint:** `/books/upload/`

Example cURL Command:
 ```bash
 curl -X POST 'http://localhost:8000/books/upload/' \
      -F 'file=@{path_to_file}' \
      -F 'data={"name":"book name","author":"book author","date_published":"01.01.2024"}'
 ```

### 4. Download the File Associated with a Book

- **Method:** GET
- **Endpoint:** `/books/{book_id}/download/`

Example cURL Command:
 ```bash
 curl -X POST 'http://localhost:8000/books/1/download/'
 ```

## Development Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the API server:
   
- Run local server (needs local DB or DB in a Docker):
  ```bash
  gunicorn app:create_app --bind 0.0.0.0:8000 --worker-class aiohttp.worker.GunicornWebWorker
  ```

- Run in a Docker:
  ```bash
  docker compose -f docker-compose.yaml up --build -d
  ```


## Testing Setup

1. Install dependencies:
   ```bash
   pip install -r requirements-test.txt
   ```
2. Run database:
   ```bash
   docker compose -f docker-compose.yaml up --build -d postgres
   ```
3. Run tests
   ```bash
   ./tests_start.sh
   ```
