from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from . import views

# Create the router
router = DefaultRouter()

# Register the BookViewSet
router.register(r"books_all", views.BookViewSet, basename="book_all")   # The r in r'books_all' denotes a raw string in Python. Without the r, '\' would be interpreted as a newline character.
views.BookViewSet
urlpatterns = [
    path("books/", views.BookList.as_view(), name="book-list"),  # Maps to the BookList view
    path("", include(router.urls)),
    path("api-token-auth/", obtain_auth_token, name="api-token-auth")
]

"""
Automatically generates URL patterns for all CRUD operations,
No need to manually define paths for CRUD operations.:
-> GET /api/books_all/: List all books.
-> POST /api/books_all/: Create a new book.
-> GET /api/books_all/<id>/: Retrieve a specific book by its ID.
-> PUT /api/books_all/<id>/: Update a book.
-> DELETE /api/books_all/<id>/: Delete a book.
"""