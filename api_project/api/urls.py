from django.urls import path, include
from .views import BookList, BookViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()

router.register(r'books_all', BookViewSet, basename='books_all')

urlpatterns = [
    path('token/', obtain_auth_token, name="api-token-auth"),
    path("books/", BookList.as_view(), name="book-list"),
    path("", include(router.urls)),
]