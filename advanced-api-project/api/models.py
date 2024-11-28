from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="Author Name")

    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=150, verbose_name="Book Title")
    publication_year = models.IntegerField(verbose_name="Publication Year")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="books", verbose_name="Author")

    def __str__(self):
        return f"{self.title} by {self.author} published in {self.publication_year}"