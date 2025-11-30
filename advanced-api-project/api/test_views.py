from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Authenticate user
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")

        # Sample books
        self.book1 = Book.objects.create(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            publication_year=1925
        )
        self.book2 = Book.objects.create(
            title="1984",
            author="George Orwell",
            publication_year=1949
        )

        self.list_url = reverse("book-list")          # GET, POST
        self.detail_url = reverse("book-detail", args=[self.book1.id])  # GET, PUT, DELETE

    # -------------------------
    # CRUD TESTS
    # -------------------------

    def test_create_book(self):
        data = {
            "title": "The Art of War",
            "author": "Sun Tzu",
            "publication_year": 500
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, "The Art of War")

    def test_get_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_book(self):
        data = {"title": "The Great Gatsby Updated"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "The Great Gatsby Updated")

    def test_delete_book(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # -------------------------
    # FILTERING, SEARCHING, ORDERING
    # -------------------------

    def test_filter_books_by_author(self):
        response = self.client.get(self.list_url + "?author=George Orwell")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["author"], "George Orwell")

    def test_search_books(self):
        response = self.client.get(self.list_url + "?search=Gatsby")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "The Great Gatsby")

    def test_order_books_by_publication_year(self):
        response = self.client.get(self.list_url + "?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # First result must be oldest (1925)
        self.assertEqual(response.data[0]["publication_year"], 1925)

    # -------------------------
    # AUTHENTICATION TEST
    # -------------------------

    def test_unauthenticated_user_cannot_access(self):
        client = APIClient()
        response = client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
