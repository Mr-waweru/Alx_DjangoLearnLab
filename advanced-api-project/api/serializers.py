from rest_framework import serializers
from .models import Book, Author
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book    # Specifies the model this serializer is for
        fields = "__all__"  # Include all fields in the serialization

    """Custom validation to ensures the publication year is not in the future"""
    def validate(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ["name", "books"]  # Includes only the name field and related books.