from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required

from .models import Book
from .forms import ExampleForm

# Create your views here.
@permission_required("bookshelf.can_edit", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "book_list.html",{
        "books": books
    })


@permission_required("bookshelf.can_create", raise_exception=True)
def add_book(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
        else:
            form = ExampleForm()
        
        return render(request, "form_demmo.html", {
            "form": form
        })
    

@permission_required("bookshelf.can_view", raise_exception=True)
def view_books(request):
    books = Book.objects.all()
    return render(request, "all_books.html", {
        "books": books
    })


@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_books(request):
    return render(request, "delete_books.html")
