from django.db import models
from datetime import datetime

# Author model represents a single author in the system.
# One Author can be associated with multiple Book objects.
class Author(models.Model):
    # Stores the author's full name as text.
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Book model represents a published book.
# Each book MUST be linked to one author -> One-to-Many relationship
class Book(models.Model):
    # Title of the book
    title = models.CharField(max_length=200)

    # Year the book was published
    publication_year = models.PositiveIntegerField()

    # ForeignKey establishes one-to-many relation:
    # One author can have many books
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
