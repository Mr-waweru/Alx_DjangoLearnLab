from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.ListView.as_view(), name="book_list"),
    path("books/<int:pk>/", views.DetailView.as_view(), name="book_detail"),
    path("books/create/", views.CreateView.as_view(), name="book_create"),
    path('books/update/<int:pk>/', views.UpdateView.as_view(), name='book_update'),
    path('books/delete/<int:pk>/', views.DeleteView.as_view(), name='book_delete'),  
]