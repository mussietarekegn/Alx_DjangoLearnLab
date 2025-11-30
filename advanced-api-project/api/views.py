from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend 
from .models import Book
from .serializers import BookSerializer
from django_filters import rest_framework
from rest_framework import generics, permissions, filters

# ----------------------------
# ListView - Retrieve all books
# ----------------------------
class BookListView(generics.ListAPIView):
    """
    GET /books/
    Returns a list of all Book instances.
    Read-only access, open to any user.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Unauthenticated users can view

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering: fields available for exact match or lookups
    filterset_fields = ['title', 'publication_year', 'author']

    # Search: fields for text search (case-insensitive, partial matches)
    search_fields = ['title', 'author__name']

    # Ordering: allow ordering results by these fields
    ordering_fields = ['title', 'publication_year', 'author']
    ordering = ['title']  # Default ordering

    def get_queryset(self):
        queryset = Book.objects.all()
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(publication_year=year)
        return queryset


# ----------------------------
# DetailView - Retrieve a single book by ID
# ----------------------------
class BookDetailView(generics.RetrieveAPIView):
    """
    GET /books/<int:pk>/
    Returns details of a single Book instance identified by primary key (pk).
    Read-only access, open to any user.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# ----------------------------
# CreateView - Add a new book
# ----------------------------
class BookCreateView(generics.CreateAPIView):
    """
    POST /books/create/
    Creates a new Book instance.
    Restricted to authenticated users only.
    Handles data validation automatically via BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# ----------------------------
# UpdateView - Modify an existing book
# ----------------------------
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT /books/update/<int:pk>/
    Updates an existing Book instance.
    Restricted to authenticated users.
    Performs full validation through BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# ----------------------------
# DeleteView - Remove a book
# ----------------------------
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /books/delete/<int:pk>/
    Deletes a Book instance identified by pk.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
