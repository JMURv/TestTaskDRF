import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.conf import settings
from mixer.backend.django import mixer

from api.models import Book

user_models = get_user_model()


@pytest.fixture(scope='function')
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(api_client):
    user = mixer.blend('api.Author', first_name='John', last_name="Doe")
    api_client.force_authenticate(user=user)
    return user


@pytest.fixture
def author_factory():
    return mixer.blend('api.Author')


@pytest.fixture
def get_author(first_name):
    return mixer.blend('api.Author', first_name=first_name)


@pytest.fixture
def book_factory():
    return mixer.cycle(3).blend('api.Book')


@pytest.fixture
def author_book(**kwargs):
    return Book.objects.create(**kwargs)


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': settings.BASE_DIR / 'db.sqlite3',
        'ATOMIC_REQUESTS': True,
    }
