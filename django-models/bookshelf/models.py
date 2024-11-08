from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_year = models.IntegerField(null=True)

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, Publication_Year: {self.publication_year}"