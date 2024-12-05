from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, Author
from django.contrib.auth.models import User

class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test user
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Log in the test user
        self.client.login(username="testuser", password="password123")

        # Create a test author
        self.author = Author.objects.create(name="Test Author")

        # Create a test book
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2022,
            author=self.author,
            added_by=self.user
        )

        # Define API endpoints matching the checker's URLs
        self.list_url = "/api/books/"
        self.detail_url = f"/api/books/{self.book.id}/"
        self.create_url = "/api/books/create/"
        self.update_url = f"/api/books/update/{self.book.id}/"
        self.delete_url = f"/api/books/delete/{self.book.id}/"

    def test_create_book(self):
        """Test creating a new book."""
        data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author.id,
            "added_by": self.user.id,
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)  # New book created
        self.assertEqual(Book.objects.last().title, "New Book")

    def test_retrieve_book(self):
        """Test retrieving a book by ID."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Book")

    def test_update_book(self):
        """Test updating a book."""
        data = {
            "title": "Updated Test Book",
            "publication_year": 2022,
            "author": self.author.id,
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()  # Reload the book from the database
        self.assertEqual(self.book.title, "Updated Test Book")

    def test_delete_book(self):
        """Test deleting a book."""
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)  # Book deleted

    def test_filter_books_by_title(self):
        """Test filtering books by title."""
        response = self.client.get(f"{self.list_url}?title=Test Book")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Book")

    def test_search_books_by_author_name(self):
        """Test searching books by author name."""
        response = self.client.get(f"{self.list_url}?search=Test Author")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["author"], self.author.id)

    def test_order_books_by_title(self):
        """Test ordering books by title."""
        # Create another book
        Book.objects.create(
            title="Another Book",
            publication_year=2021,
            author=self.author
        )
        response = self.client.get(f"{self.list_url}?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Another Book")

    def test_order_books_by_publication_year_descending(self):
        """Test ordering books by publication year (descending)."""
        # Create another book
        Book.objects.create(
            title="Older Book",
            publication_year=2020,
            author=self.author
        )
        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Test Book")  # Most recent