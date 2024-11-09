from django.urls import path

from . import views
from .views import list_books, LibraryDetailView, login_view, logout_view, register

urlpatterns = [
    path("books", views.list_books, name="list_books"),
    path("library/<int:pk>", views.LibraryDetailView.as_view(), name="library_detail"),
    path('login/', views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path("register", views.register, name="register"),
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
]