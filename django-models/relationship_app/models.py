from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    class Meta:
        permissions = [
            ("can_add_book", "Can add a book"),
            ("can_change_book", "Can edit a book"),
            ("can_delete_book", "Can delete a book"),
        ]
        
    def __str__(self):
        return f"{self.title} by {self.author}"
    

class Library(models.Model):
    name = models.CharField(max_length=60)
    books = models.ManyToManyField(Book, related_name="libraries")

    def __str__(self):
        return self.name
    

class Librarian(models.Model):
    name = models.CharField(max_length=60)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name="librarian")

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    USER_ROLES = [
        ("Admin", "Admin"),
        ("Librarian", "Librarian"),
        ("Member", "Member"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=USER_ROLES)

    def __str__(self):
        return f"{self.user} - {self.role}"