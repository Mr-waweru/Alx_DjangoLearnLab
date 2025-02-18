from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"posts", views.PostViewSet, basename="post")
router.register(r"comments", views.CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)), # Include all routes automatically generated by the router
    path("feed/", views.PostViewSet.as_view({"get": "feed"}), name="feed"), # Custom endpoint for fetching a user's feed
    path("posts/<int:pk>/like/", views.PostViewSet.as_view({"post": "like"}), name="post-like"), # Endpoint for liking a specific post (uses PostViewSet's `like` action)
    path("posts/<int:pk>/unlike/", views.PostViewSet.as_view({"delete": "unlike"}), name="post-unlike"), # Endpoint for unliking a specific post (uses PostViewSet's `unlike` action)
]