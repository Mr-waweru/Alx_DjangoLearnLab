from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("profile/", views.UserDetailView.as_view(), name="profile"),
    path("follow/<int:pk>/", views.FollowUserView.as_view(), name="follow_user"),   # <int:user_id>
    path("unfollow/<int:pk>/", views.UnfollowUserView.as_view(), name="unfollow_user"),  # <int:user_id>
]