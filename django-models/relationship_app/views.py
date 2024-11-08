from typing import Any
from django.shortcuts import render
from django.views.generic import DetailView

from .models import *

# Create your views here.
def list_all_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {
        "books": books
    })


# Create a class-based view in relationship_app/views.py that displays details for a specific library, listing all books available in that library.
# Utilize Django’s ListView or DetailView to structure this class-based view.
class LibraryDetail(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context