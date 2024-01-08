import pytest


# class TestBookViews:

@pytest.mark.asyncio
async def test_get_book_list(test_client):
    # Positive test case
    response = await test_client.post('/books/', json={})
    assert response.status == 200
    data = await response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_book(test_client):
    # Positive test case
    response = await test_client.get('/book/1/')
    assert response.status == 200
    data = await response.json()
    print('DATA!!!!!!!!!!!!!', data)
    assert isinstance(data, dict)
    assert len(data) == 3

    # Negative test case
    response = await test_client.get('/book/invalid_id/')
    assert response.status == 404


@pytest.mark.asyncio
async def test_create_book(test_client):
    # Positive test case
    # with open('test_file.pdf', 'wb') as f:
    #     f.write(b'test content')
    data = {
        'name': 'Test Book',
        'author': 'Test Author',
        'date_published': '01.01.2024'
    }
    response = await test_client.post('/book/upload/', data=data, files={'file': open('test_book.pdf', 'rb')})
    assert response.status == 201
    data = await response.json()
    assert 'book_id' in data

    # Negative test case
    response = await test_client.post('/book/upload/', data="invalid_data")
    assert response.status == 400

    # os.remove('test_file.pdf')
