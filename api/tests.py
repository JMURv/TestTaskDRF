import pytest
from rest_framework.reverse import reverse
from .models import Book, Author
from .serializers import AuthorSerializer
from conftest import author_book


@pytest.mark.django_db
def test_get_all_books(api_client, book_factory):
    books = book_factory
    response = api_client.get('/api/books/')
    assert response.status_code == 200
    assert len(response.data) == len(books)


@pytest.mark.django_db
def test_create_book(api_client, authenticated_user):
    author = AuthorSerializer(authenticated_user)
    url = reverse('book_list')
    data = {
        'title': 'Test Book',
        'description': 'Test Description',
        'publication_date': '2022-01-01',
        'author': author.data,
    }
    response = api_client.post(url, data=data, format='json')
    assert response.status_code == 201
    assert Book.objects.count() == 1
    book = Book.objects.first()
    assert book.title == 'Test Book'
    assert book.author.id == author.data.get('id')
    assert book.description == 'Test Description'
    assert book.publication_date.strftime('%Y-%m-%d') == '2022-01-01'

    # Проверяем выдает ли 400, если авторизованный пользователь - не автор книги
    data = {
        'title': 'Test Book',
        'description': 'Test Description',
        'publication_date': '2022-01-01',
        'author': "Not Author",
    }
    response = api_client.post(url, data=data, format='json')
    assert response.status_code == 400
    assert Book.objects.count() == 1


@pytest.mark.django_db
def test_get_book(api_client, book_factory):
    book = book_factory[0]
    response = api_client.get(f'/api/books/{book.id}/')

    assert response.status_code == 200
    assert response.data['id'] == book.id
    assert response.data['title'] == book.title
    assert response.data['description'] == book.description
    assert response.data['publication_date'] == book.publication_date.isoformat()

    assert response.data['author']['id'] == book.author.id
    assert response.data['author']['first_name'] == book.author.first_name
    assert response.data['author']['last_name'] == book.author.last_name


@pytest.mark.django_db
def test_update_book(api_client, authenticated_user, book_factory, author_factory):
    for book in book_factory:
        new_author = AuthorSerializer(author_factory).data
        new_data = {
            'title': 'New Book Title',
            'author': new_author,
            'description': 'New Book Description',
            'publication_date': '2022-05-01'
        }
        url = reverse('book_detail', kwargs={'pk': book.id})
        response = api_client.put(url, data=new_data, format='json')

        assert response.status_code == 200
        assert response.data['title'] == new_data['title']
        assert response.data.get('author').get('first_name') == new_author.get('first_name')
        assert response.data['description'] == new_data['description']
        assert response.data['publication_date'] == new_data['publication_date']


@pytest.mark.django_db
def test_delete_book(api_client, authenticated_user, book_factory):
    book = book_factory[0]

    url = reverse('book_detail', kwargs={'pk': book.id})
    response = api_client.delete(url)

    assert response.status_code == 204
    assert Book.objects.count() == 2
