from django.urls import path

from . import views

urlpatterns = [
    path("books", views.list_all_books, name="list_all_books"),
    path("library/<int:pk>", views.LibraryDetail.as_view(), name="library_detail")
]