from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


# Create your views here.

# ListView: Retrieve all books
class ListView(generics.ListAPIView):
    """
    Handles GET requests to retrieve a list of all books.
    Open to all users (unauthenticated users can access this view).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny] # Read-only access for everyone


# DetailView: Retrieve a single book by ID
class DetailView(generics.RetrieveAPIView):
    """
    Handles GET requests to retrieve a single book by its primary key (ID).
    Open to all users (unauthenticated users can access this view).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny] # Read-only access for everyone
    

# CreateView: Add a new book
class CreateView(generics.CreateAPIView):
    """
    Handles POST requests to create a new book.
    Only authenticated users are allowed to add new books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict access to authenticated users
    
    def perform_create(self, serializer):
        """
        Custom save behavior: Associates the currently 
        authenticated user with the book being created.
        """
        serializer.save(added_by=self.request.user)  # Save the user who submitted the request

# UpdateView: Modify an existing book
class UpdateView(generics.UpdateAPIView):
    """
    Handles PUT/PATCH requests to update an existing book by its ID.
    Only authenticated users are allowed to update books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict access to authenticated users

    def perform_update(self, serializer):
        """
        Custom update behavior: Ensures only the user who created the book or an admin can modify it.
        """
        if not self.request.user.is_superuser and self.get_object().added_by != self.request.user:
            raise PermissionDenied("You do not have permission to edit this book.")
        serializer.save()
    

# DeleteView: Remove a book
class DeleteView(generics.DestroyAPIView):
    """
    Handles DELETE requests to delete a book by its ID.
    Only authenticated users are allowed to delete books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict access to authenticated users

    def perform_destroy(self, instance):
        """
        Custom delete behavior: Ensures only the user who created the book or an admin can delete it.
        """
        if not self.request.user.is_superuser and instance.added_by != self.request.user:
            raise PermissionDenied("You do not have permission to delete this book.")
        instance.delete()