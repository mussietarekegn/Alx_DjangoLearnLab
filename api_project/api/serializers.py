from rest_framework import serializers
from .models import Book
from django.utils import timezone

class BookSerializer(serializers.ModelSerializer):
    published_date = serializers.DateField(default=lambda: timezone.now().date())

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['published_date']
