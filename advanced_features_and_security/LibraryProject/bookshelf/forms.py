from django.forms import ModelForm
from .models import Book

class BookForm(ModelForm):
	class Meta:
		model = Book
		fields = '__all__'

class ExampleForm(ModelForm):
	class Meta:
		model = Book
		fields = ['title', 'author']