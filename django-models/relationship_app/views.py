from typing import Any
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test


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
def has_role(user, role):
    return user.userprofile.role == role

# Admin view, only accessible to users with the "Admin" role
@user_passes_test(lambda user: has_role(user, "Admin"))
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

# Librarian view, only accessible to users with the "Librarian" role
@user_passes_test(lambda user: has_role(user, "Librarian"))
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

# Member view, only accessible to users with the "Member" role
@user_passes_test(lambda user: has_role(user, "Member"))
def member_view(request):
    return render(request, "relationship_app/member_view.html")
