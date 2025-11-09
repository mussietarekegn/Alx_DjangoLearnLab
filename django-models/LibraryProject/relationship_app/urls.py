from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import list_books, LibraryDetailView, admin_view, member_view, librarian_view, add_book, edit_book, delete_book

urlpatterns = [
    # Books and library
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    path('books/add/', add_book, name='add_book'),          # <-- add_book/
    path('books/<int:pk>/edit/', edit_book, name='edit_book'),  # <-- edit_book/
    path('books/<int:pk>/delete/', delete_book, name='delete_book'),

    # Authentication URLs
    path('register/', views.register, name='register'),  # Must be exactly views.register
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),


    path('admin-dashboard/', admin_view, name='admin_view'),
    path('librarian-dashboard/', librarian_view, name='librarian_view'),
    path('member-dashboard/', member_view, name='member_view'),
]
