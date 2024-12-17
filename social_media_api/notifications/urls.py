from django.urls import path
from .views import NotificationViewSet

notification_list = NotificationViewSet.as_view({
    "get": "list",
    "post": "create"
})

notification_detail = NotificationViewSet.as_view({
    "get": "retrieve",
    "delete": "destroy"
})

urlpatterns = [
    path("", notification_list, name="notification-list"),
    path("<int:pk>/", notification_detail, name="notification-detail"),
    path("mark_as_read/", NotificationViewSet.as_view({"post": "mark_as_read"}), name="notification-mark-as-read"),
]

"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

router = DefaultRouter()
router.register("notifications", NotificationViewSet, basename="notifications")

urlpatterns = [
    path("", include(router.urls)),
]
"""