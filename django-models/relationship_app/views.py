from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django import forms


from .models import Book
from .models import Library

# Create your views here.
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {
        "books": books
    })


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context
    

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("login"))
    else:
        form = UserCreationForm()

    return render(request, "relationship_app/register.html",{
        "form": form
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(""))
        else:
            return render(request, "relationship_app/login.html",{
                "message": "Invalid Credentials."
            })
        
    return render(request, "relationship_app/login.html")


def logout_view(request):
    logout(request)
    return render(request, "relationship_app/login.html", {
        "message": "Logged out"
    })


# Check if the user has a specific role
def check_role(user, role):
     return user.is_authenticated and hasattr(user, "userprofile") and user.userprofile.role == role

# Admin view
@user_passes_test(lambda user: check_role(user, "Admin"))
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

# Librarian view
@user_passes_test(lambda user: check_role(user, "Librarian"))
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

# Member view
@user_passes_test(lambda user: check_role(user, "Member"))
def member_view(request):
    return render(request, "relationship_app/member_view.html")



"""
# Helper function to check if the user is an Admin
def is_admin(user):
    return user.userprofile.role == 'Admin'

# Helper function to check if the user is a Librarian
def is_librarian(user):
    return user.userprofile.role == 'Librarian'

# Helper function to check if the user is a Member
def is_member(user):
    return user.userprofile.role == 'Member'

# Admin view, only accessible to users with the 'Admin' role
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian view, only accessible to users with the 'Librarian' role
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member view, only accessible to users with the 'Member' role
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')
"""


"""
def is_admin(user):
    return user.userprofile.role == "Admin"

def is_librarian(user):
    return user.userprofile.role == "Librarian"

def is_member(user):
    return user.userprofile.role == "Member"

# Admin view
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

# Librarian view
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

# Member view
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")
"""

#BookForm for demonstration
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author"]

# List books view (no permission required for viewing)
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html",{
        "books": books
    })
# Add book view; only accessible to users with the "can_add_book" " permission
@permission_required("relationship_app.can_add_book", raise_exception=True)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm()
    return render (request, "relationship_app/add_book.html", {
        "form": form
    })


# Edit book view; only accessible to users with the "can_change_book" permission
@permission_required("relationship_app.can_change_book", raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = BookForm(request.POST or None, instance=book)
    
    if form.is_valid():
        form.save()
        return redirect("list_books")

    return render(request, "relationship_app/edit_book.html", {
        "form": form
    })


# Delete book view; only accessible to users with the "can_delete_book" permission
@permission_required("relationship_app.can_delete_book", raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("list_books")
    
    return render(request, "relationship_app/delete_book_confirm.html", {
        "book": book
    })

