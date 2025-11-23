from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# Create your views here.


class BookList(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = BookSerializer
    queryset = Book.objects.all()
