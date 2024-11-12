<!-- Retrieve the book you created -->
book = Book.objects.get(title="1984")
print(book)