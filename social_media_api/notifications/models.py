from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType  # Allows you to refer to any model in your project dynamically
# from django.contrib.auth import get_user_model

# User = get_user_model()

# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")  # The user who will see the notification
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="actor_notifications")  # A user who liked or commented
    verb = models.CharField(max_length=100) # Action that triggered the notification (e.g., "liked", "commented")
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True) # Type of object (model) that the notification is about. (Eg. Post or a Comment)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)   # stores the ID of the specific object related to the notification
    target = GenericForeignKey("target_content_type", "target_object_id")
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.actor} {self.verb} {self.target} for {self.recipient}"
    """
    target = GenericForeignKey('target_content_type', 'target_object_id')
    This combines the two fields above to create a generic relationship.

    - The target_content_type tells it what model the object is (Post, Comment, etc.).
    - The target_object_id tells it which specific instance of that model (e.g., Post ID 5 or Comment ID 12).
    Together, they allow the Notification model to link to any model instance in your project.
    """