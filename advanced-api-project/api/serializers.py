from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


# Serializes the Book model fields into JSON format.
# Contains custom validation to prevent publication dates in the future.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom validation to ensure the publication year is not greater than current year.
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# Serializes Author data including a nested list of their books.
# Demonstrates handling of one-to-many relationships.
class AuthorSerializer(serializers.ModelSerializer):
    # Nested BookSerializer to dynamically serialize each author's books
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
