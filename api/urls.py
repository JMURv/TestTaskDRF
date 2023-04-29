from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookList, BookDetail

urlpatterns = [
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('books/', BookList.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book_detail'),
]
