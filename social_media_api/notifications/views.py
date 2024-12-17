from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import NotificationSerializer

# Create your views here.
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-timestamp')
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter notifications to show only those for the logged-in user"""
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_as_read(self, request):
        user = request.user
        notifications = Notification.objects.filter(recipient=user, read=False)
        notifications.update(read=True)
        return Response({"detail": "Notifications marked as read."}, status=status.HTTP_200_OK)