<!-- Delete the book -->
book.delete()

<!-- Confirm deletion by retrieving all books -->
all_books = Book.objects.all()
print(all_books)