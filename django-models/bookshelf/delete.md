<!-- Delete the book -->
from bookshelf.models import Book
book.delete()

<!-- Confirm deletion by retrieving all books -->
all_books = Book.objects.all()
print(all_books)