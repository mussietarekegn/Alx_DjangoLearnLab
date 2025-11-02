from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'author', 'pulication_year')
  search_fields = ["title", "author"]
  list_filter = ["publication_year"]

admin.site.register(Book, BookAdmin)
